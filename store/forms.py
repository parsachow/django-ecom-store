from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import OrderItem

class CustomUserForm(UserCreationForm):
    #adding extra fields
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "name")

class CartAddForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']