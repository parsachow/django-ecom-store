from django.urls import path
from .views import cart, cart_add, cart_update, cart_delete


urlpatterns = [
   path('', cart, name='cart'),
   path('add/', cart_add, name='cart_add'),
   path('update/', cart_update, name='cart_update'),
   path('delete/', cart_delete, name='cart_delete'),
]