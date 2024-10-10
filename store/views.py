from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import CustomUserForm
from .models import Category, Customer, Product, Order, OrderItem

# Create your views here.
    
class Login(LoginView):
    template_name = "auth/login.html"
    success_url = reverse_lazy("home")

class Logout(LogoutView):
    success_url = reverse_lazy("login")

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # error_message = 'Invalid Signup'
            print(form.errors)
    #if bad POST/GET request, render empty signup form
    form = CustomUserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'auth/signup.html', context)



class Home(ListView):
    model = Product
    paginate_by = 8
    template_name = 'home.html'  

class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'

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
    