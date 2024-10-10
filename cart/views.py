from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .cart import Cart
from store.models import Product

# Create your views here.
def cart(request):
    return render(request, "cart.html", {})
    
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get product id
        product_id = int(request.POST.get('product_id'))
        # lookup whether product exists in DB
        product = get_object_or_404(Product, id=product_id)
        # save to session/add product to cart
        cart.add(product=product)
        # response = JsonResponse({'Prodcuct Name': product.name})
        # return response
    
    
def cart_update(request):
    pass
    
def cart_delete(request):
    pass

