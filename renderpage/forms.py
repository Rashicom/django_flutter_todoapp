from django.forms import ModelForm
from django import forms
from api.models import CustomUser

class signupform(ModelForm):
    confirm_password = forms.CharField(widget=(forms.PasswordInput(attrs= {'class':'form-control bg-transparent my-3', 'placeholder': 'Confirm password'})), label='')
    class Meta:
        model = CustomUser
        fields = ["email", "contact_number","first_name", "password",]
        
        widgets = {
            "email": forms.EmailInput(attrs = {'class':'form-control bg-transparent my-3', 'placeholder': 'Email'}),
            "contact_number": forms.TextInput(attrs = {'class':'form-control bg-transparent my-3', 'placeholder': 'Contact number'}),
            "first_name": forms.TextInput(attrs = {'class':'form-control bg-transparent my-3', 'placeholder': 'Name'}),
            "password": forms.PasswordInput(attrs = {'class':'form-control bg-transparent my-3', 'placeholder': 'Password'}),  
            
        }
        
        labels = {
            "email":"",
            "contact_number": "",
            "first_name": "",
            "password": "",
            
            
        }
        