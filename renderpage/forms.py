from django.forms import ModelForm
from django import forms
from api.models import CustomUser, tasks

class signupform(ModelForm):
    confirm_password = forms.CharField(widget=(forms.PasswordInput(attrs= {'class':'form-control bg-transparent my-3', 'id':'id_confirm_password', 'placeholder': 'Confirm password'})), label='')
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
        

# form for rendiring add_taks
class add_task_form(ModelForm):

    class Meta:
        model = tasks
        fields = ['email','task','task_details','task_due_date','task_due_time']
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control bg-transparent my-3', 'placeholder': 'Email'}),
            'task':forms.TextInput(attrs={'class':'form-control bg-transparent my-3', 'placeholder': 'task'}),
            'task_details':forms.TextInput(attrs={'class':'form-control bg-transparent my-3', 'placeholder': 'task_details'}),
            'task_due_date':forms.DateInput(attrs={'class':'form-control bg-transparent my-3', 'placeholder': 'task_due_date'}),
            'task_due_time':forms.TimeInput(attrs={'class':'form-control bg-transparent my-3', 'placeholder': 'task_due_time'}),
        }

        labels = {
            "email":"",
            "task":"",
            "task_details":"",
            "task_due_date":"",
            "task_due_time":"",


            
        }