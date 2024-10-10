from .cart import Cart

#context processor to make our cart work on all pages
def cart(request):
    return {'cart': Cart(request)}



#check session info in shell after copying the sessionID key from browser-> application-> cookies

# # session key example - qw56q1ejp0tj7vlfiqtthahcnib2tfdr

# python3 manage.py shell
# from django.contrib.sessions.models import Session
# session_key = Session.objects.get(pk='qw56q1ejp0tj7vlfiqtthahcnib2tfdr')
# session_key.get_decoded()

