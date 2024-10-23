from store.models import *
from decimal import Decimal



class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #get current session key if the user is returning user and the key already exists
        cart = self.session.get('session_key')
        
        #if it doesn't exist, they create session_key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart
    
    def add(self, product, quantity):
        #string format product.id is taken since django uses json for serializing session data and json only allows string key names
        product_id = str(product.id)
        product_quantity = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]={'price': str(product.price)}
            self.cart[product_id]=int(product_quantity)
    
        self.session.modified = True
    
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
   
    # for 1 individual product
    def get_product_quantities(self):
        quantities = self.cart.values()
        return quantities
    
    
    def get_total_cart_products(self):
        quantity = self.cart.values()
        total = sum(quantity)
        return total
    
    
    def get_total_products_price(self, product, quantity):
        
        # indv product price * product quantity
        pass
                
    
    def get_cart_totalprice(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value)
        return total
    
    #get total number of products in cart
    def __len__(self):
        return len(self.cart)
    
    
    def delete_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True