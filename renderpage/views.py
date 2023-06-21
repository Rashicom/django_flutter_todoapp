from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import signupform

# Create your views here.

class login(View):

    def get(self, request):
        return render(request,'login.html')

    def post(self, request):
        pass


class signup(View):

    def get(self, request):
        registerform = signupform
        return render(request, 'signup.html',{"form": registerform})

    def post(self, request):
        pass


class home(View):

    def get(self, request):
        return render(request, 'todoapp.html')