from django.urls import path
from .views import Home, signup, Login, Logout, ProductDetail, category_detail, search_product, checkout

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('category/<str:foo>', category_detail, name='category_detail'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', search_product, name='search_product'),
    path('checkout/', checkout, name='checkout'),
]