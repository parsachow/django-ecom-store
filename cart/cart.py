class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #get current session key if the user is returning user and the key already exists
        cart = self.session.get('session_key')
        
        #if it doesn't exist, they create session_key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart
    
    def add(self, product):
        product_id = str(product.id)
        self.cart[product_id] = {'price': str(product.price)}
        
        self.session.modified = True
        