from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json


from .forms import CustomUserForm, CartAddForm
from .models import Category, User, Product, Order, OrderItem

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
    
    #UnorderedObjectListWarning can be overriden by adding a datetimefield to the model, then ordering the queryset by that field
    
    

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    # cart_add = CartAddForm()
    return render(request, 'product_detail.html', {'product':product})


def category_detail(request, foo):
    category = Category.objects.get(product_type=foo)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', { 'products': products, 'category': category })


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
    # once order is placed - order completed = true
    # get orderitems info
    # get shipping info
    
    return render(request, 'checkout.html')



#orderhistory - orders placed(created) filtered by user
# def order_history(request, id):
#     # filter(user=user)
#     order = Order.objects.get(id=id) 
#     order_items = OrderItem.objects.filter(order=order)
#     return render(request, 'order_histort.html', {'order': order, 'order_items': order_items})
    
