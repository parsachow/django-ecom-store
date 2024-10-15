from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



from .cart import Cart
from store.models import Product, Order, User


def cart(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cart_quantities = cart.get_product_quantities
    cart_total = cart.get_cart_totalprice
    
    return render(request, 'cart.html/', {"cart_products": cart_products, "cart_quantities": cart_quantities, "cart_total": cart_total,})



def cart_add(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        #get product id
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        
        # lookup whether product exists in DB
        product = get_object_or_404(Product, id=product_id)
        
        #save to session/add product to cart
        cart.add(product=product, quantity=product_quantity)
        total_cart_qty = cart.__len__()
        
        
        response = JsonResponse({'total_cart_qty': total_cart_qty })
        return response
    
    
    
def cart_update(request):
    pass
    
def cart_delete(request):
    pass

