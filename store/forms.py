from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    #adding extra fields
    email = forms.EmailField()
    name = forms.CharField()
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "name")