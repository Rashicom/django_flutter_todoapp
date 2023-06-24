from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import task_serializer,  user_serializer, login_serializer
from .models import tasks, CustomUser
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.


# user login
class user_login(APIView):
    serializer_class = login_serializer

    def post(self, request, format = None):
        """
        serialing the data and validating it, any exception found is_valied()
        the functionn automatically return respond with the error message as a dictionery
        """

        # serializing data
        serializer = self.serializer_class(data=request.data)

        # validating the data
        serializer.is_valid(raise_exception=True)

        # authenticate the user
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email = email, password = password)
        
        # if user is authenticated create tocken
        if user:
            token, created = Token.objects.get_or_create(user = user)
            return Response({"status":200, "email": email, "token": token.key}, status=200)

        # else return 401 unautherized message
        else:
            return Response({"status":401,"message":"invalied credencials"}, status=401)   




# user signup
class user_signup(APIView):
    serializer_class = user_serializer

    def post(self, request, format = True):
        """
        serializing the recieved data and and validate the data
        if any exception found it returden with the exception error message
        """
        print(request.data)
        # serializing data
        serialized_data = user_serializer(data = request.data)
        
        # if the data is valied create user
        if serialized_data.is_valid():
            
            # create new user
            CustomUser.objects.create_user(
                                            email=serialized_data.data['email'],
                                            contact_number = serialized_data.data['contact_number'],
                                            first_name = serialized_data.data['first_name'],
                                            password = serialized_data.data['password']
                                        )
            # return secsuss response
            return Response(serialized_data.data, status=201)
        
        # if any exception found return with the exception message
        else:
            
            # returning the message inside .errors which holds the exceptonal messages
            return Response(serialized_data.errors, status=403)


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
            



class check(APIView):

    def get(self, request, format=None):
        return Response({"check":"check_success"})     
        