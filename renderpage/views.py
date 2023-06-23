from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import signupform, add_task_form

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
        print("form submission")
        pass


class home(View):

    def get(self, request):
        return render(request, 'todoapp.html')



# add task
class add_task(View):

    def post(self, request):
        pass

    def get(self, request):
        addtaskform = add_task_form
        return render(request, 'add_task.html',{"form":addtaskform})