from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import task_serializer
from .models import tasks

# Create your views here.


# user login
class user_login(APIView):
    
    def post(self, request, format = None):
        return Response({"status":"user_login"})


# user signup
class user_signup(APIView):

    def post(self, request, format = True):
        return Response({"status":"user_signup"})


# returning all task_list
class task_list_all(APIView):
    """
    returning all the tasks of the perticular user
    this is not returning for specific dates
    """
    def get(self, request, format=None):
        snippets = tasks.objects.all()
        serialized_data = task_serializer(snippets, many = True)
        return Response(serialized_data.data)


class addtask(APIView):
    
    def post(self, requset, format=None):
        print("request hit")
        serialized_data = task_serializer(data=requset.data)
        print(requset.data)

        if serialized_data.is_valid():
            
            print("valied")
            print(serialized_data.data)
            return Response(serialized_data.data)
        else:
            print(serialized_data.errors)
            print("not valied")
            return Response({"error":serialized_data.errors}, status=400)  
            


        
        