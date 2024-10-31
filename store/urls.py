from django.urls import path
from .views import Home, signup, Login, Logout, product_detail, category_detail, search_product, checkout, cart_update, cart, cart_add, cart_delete, order_history, order_confirmed, cancel_order

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('category/<str:foo>', category_detail, name='category_detail'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('search/', search_product, name='search_product'),
    path('cart/', cart, name='cart'),
    path('cart_add/', cart_add, name='cart_add'),
    path('cart_update/', cart_update, name='cart_update'),
    path('cart_delete/<int:item_id>', cart_delete, name='cart_delete'),
    path('checkout/', checkout, name='checkout'),
    path('order_history/', order_history, name='order_history'),
    path('order_confirmed/', order_confirmed, name='order_confirmed'),
    path('cancel_order/', cancel_order, name='cancel_order'),
]