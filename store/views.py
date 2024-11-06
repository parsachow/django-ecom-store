from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, View
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json


from .forms import CustomUserForm, CheckoutForm
from .models import Category, User, Product, Order, OrderItem, Shipping, Inventory

# Create your views here.
    
class Login(LoginView):
    template_name = "auth/login.html"
    success_url = reverse_lazy("home")

    redirect_authenticated_user = True


class Logout(LogoutView):
    success_url = reverse_lazy("login")


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Signup'
    #if bad POST/GET request, render empty signup form
    form = CustomUserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'auth/signup.html', context)


class Home(ListView):
    model = Product
    paginate_by = 8
    template_name = 'home.html'  
    
    # get quantity of items in current order by adding context to page
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        order, created = Order.objects.get_or_create(user=self.request.user, is_completed=False)
        context['cartItemsQuantity'] = order.get_total_cart_quantity
        return context
        
    #UnorderedObjectListWarning can be overriden by adding a datetimefield to the model, then ordering the queryset by that field
    
    

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # get quantity of items in current order
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    cartItemsQuantity = order.get_total_cart_quantity
    
    return render(request, 'product_detail.html', {'product':product, 'cartItemsQuantity':cartItemsQuantity})


def category_detail(request, foo):
    category = Category.objects.get(product_type=foo)
    products = Product.objects.filter(category=category)
    
    # get quantity of items in current order
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    cartItemsQuantity = order.get_total_cart_quantity
    
    return render(request, 'category_detail.html', { 'products': products, 'category': category, 'cartItemsQuantity': cartItemsQuantity })


def search_product(request):
    search_performed = False
    if request.method == "POST":
        search = request.POST['search']
        search = Product.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)|Q(color__icontains=search))
        search_performed = True
        return render(request, 'search.html', {'search': search, 'search_performed': search_performed})
    else:
        return render(request, "search.html", {})


def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    items = order.orderitem_set.all()
    cartItemsQuantity = order.get_total_cart_quantity
    cartTotalPrice = order.get_total_cart_price
    
    return render(request, 'cart.html', {'items': items, 'cartItemsQuantity': cartItemsQuantity, 'cartTotalPrice': cartTotalPrice})


def cart_add(request): 
    if request.method == "POST":
        data = request.POST
        print(data.get("product_id"))
        product_id = data["product_id"]
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product, quantity=1)
            print(orderitem)
            # orderitem.quantity += 1
            orderitem.save()
        #whenever a VIEW is getting something from the frontend, the return is always a JSONresponse 
        return JsonResponse("item added", safe=False)
    

def cart_update(request):
    if request.method == "POST":
        data = request.POST
        product_id = data["product_id"]
        action = data["action"]
        product = Product.objects.get(id=product_id)
        
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
            if action == 'add':
                orderitem.quantity += 1
                orderitem.save()
                print('item added')
        
            if action == 'delete':
                if orderitem.quantity <= 1:
                    orderitem.delete() 
                else:
                    orderitem.quantity -= 1
                    orderitem.save()
             
        #whenever a VIEW is getting something from the frontend, the return is always a JSONresponse
        return JsonResponse("item updated", safe=False)


def cart_delete(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.delete()
    # item.save()
    return redirect('cart')
        

def checkout(request):
    form = CheckoutForm()
    
    # get quantity of items in current order
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    cartItemsQuantity = order.get_total_cart_quantity
    
    return render(request, 'checkout.html', {'form':form, 'cartItemsQuantity':cartItemsQuantity})

    
# def order_confirmed(request):
#     if request.method == "POST":
#         form = CheckoutForm(request.POST)
#         #get the order
#         order = Order.objects.get(user=request.user, is_completed=False)
#         print(order)
    
#         if form.is_valid():
#             shipping = form.save(commit=False)
#             shipping.user = request.user
#             shipping.order = order
#             # shipping.payment = order.payment - How to save payment info
#             shipping.save()
#             order.is_completed = True
#             order.save()
#         return render(request, 'order_confirmed.html')

def order_confirmed(request):
    form = CheckoutForm(request.POST)
    if request.method == "POST" and form.is_valid():
         # Get current order
        order = Order.objects.filter(user=request.user, is_completed=False).first()
        # Get the associated OrderItems for the order
        order_items = order.orderitem_set.all()
    
        
        # save final/current order 
        order.is_completed = True
        order.payment = form.cleaned_data['payment'] 
        order.save()
        #save shipping info from the form
        shipping = form.save(commit=False)
        shipping.user = request.user
        shipping.order = order
        shipping.save()
        # adjust Inventory for each OrderItem
        for order_item in order_items:
            product = order_item.product
            quantity = order_item.quantity
            
            inventory = get_object_or_404(Inventory, product=product)
            if inventory.current_inventory >= quantity:
                inventory.current_inventory -= quantity
                inventory.save()
            else:
                messages.error(request, f"Not enough stock for {product.name}")
                return redirect('cart')
        return redirect('order_confirmed')
    return render(request, 'order_confirmed.html')


# orderhistory - orders placed(created) filtered by user
def order_history(request):
    orders = Order.objects.filter(user=request.user).filter(is_completed=True).order_by('-ordered_at')
    # have to make a relationship between orderitems in an order in the TEMPLATE. use 'order.orderitem.set.all' to make relationship between dbs for nested forloops. 
    order_item = OrderItem.objects.filter(order__user=request.user)
    
    # get quantity of items in current order
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    cartItemsQuantity = order.get_total_cart_quantity
    
    context = {
        'orders': orders, 
        'order_item': order_item,
        'cartItemsQuantity': cartItemsQuantity,
    }
    
    return render(request, 'order_history.html', context)




def cancel_order(request):
    if request.method == 'POST':
        data = request.POST
        order_id = data["order_id"]
        order = Order.objects.get(id=order_id, user=request.user)

        if order.status == 'Order Accepted' or 'Order Being Processed':
            order.status = 'Order Canceled'
            order.save()
            
        return render(request, 'order_history.html')
        
    # without forms, include js on frontend, eventhandler, and validation in view