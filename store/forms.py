from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Shipping

PAYMENT_CHOICES = (
    ("CC", "Credit Card"),
    ("CD", "Cash on Delivery"),
    ("PP", "Paypal")
)

class CustomUserForm(UserCreationForm):
    #adding extra fields
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "name")


class CheckoutForm(forms.ModelForm):
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES)
    
    class Meta:
        model = Shipping
        fields = ['address', 'state', 'zip', 'country', 'payment']