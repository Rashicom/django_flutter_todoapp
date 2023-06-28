from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import task_serializer,  user_serializer, login_serializer, task_list_all_serializer
from .models import tasks, CustomUser
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


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
            return Response({"status":200, "email": email, "Authorization": "Token "+token.key}, status=200)

        # else return 401 unautherized message
        else:
            return Response({"status":401,"message":"unauthorized"}, status=401)   


# logout
class user_logout(APIView):

    def get(self, request, format = None):
        """
        we have ot just delete the tocken from the tocken table using the
        user email. then return nothing. becouse it is stateless
        """
        # delete tocken from the table
        # Token.objects.get(user = request.user)
        try:
            Token.objects.get(user = request.user).delete()
            return Response(status=200)
        
        # return the same if url again called without any data
        except Exception as e:
            return Response(status=200)



# user signup
class user_signup(APIView):
    serializer_class = user_serializer

    def post(self, request, format = True):
        """
        serializing the recieved data and and validate the data
        if any exception found it returden with the exception error message
        """
        
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
    permission_classes = [IsAuthenticated]
    serializer_class = task_list_all_serializer

    def get(self, request, format=None):
        """
        returning all the tasks of the perticular user who is accessed
        returning all the task including checked tasks
        advised to use another url if u need unchecked tasks
        """
        print("request hit")
        
        # fetching all the task list of the user who is accessed
        snippets = tasks.objects.filter(email = request.user)
        print(request.user)
        #serializing the data and returning    
        serialized_data = self.serializer_class(snippets, many = True)
        return Response(serialized_data.data, status=200)



# returning the checked task only
class task_list_checked(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_list_all_serializer

    def get(self, request, format = None):
        """
        this view is filtering only checked(compleated tasks) from the data base
        and return to the user who is requested for
        """
        print("checked data")

        # fetching checked tasks list of the user who is accessed
        snippets = tasks.objects.filter(email = request.user, task_status = True)
        
        # serializing data and return
        serialized_data =  self.serializer_class(snippets, many = True)
        return Response(serialized_data.data, status=200)


# returning the unchecked task only
class task_list_unchecked(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_list_all_serializer

    def get(self, request, format = None):
        """
        this view is filtering only unchecked(uncompleated tasks) from the data base
        and return to the user who is requested for
        """
        print("unchecked data")

        # fetching unchecked task list of the user who is accessed
        snippets = tasks.objects.filter(email = request.user, task_status = False)
        
        # serializing data and return
        serialized_data =  self.serializer_class(snippets, many = True)
        return Response(serialized_data.data, status=200)



# add new task
class addtask(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        authenticated user can add task to thire task lists, if authentication
        pass
        varify the email in the body is match with the tokens matching email.
        otherwise return email is invalied
        """
        serialized_data = task_serializer(data=request.data)

        # fetching email form body to check with tocken authenticated user
        email = request.data["email"]

        # cross check for missmatch
        if str(email) != str(request.user):
            return Response({"status":"tocken and email missmatch"}, status=401)

        
        # new task added if the data is valied
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=201)
        
        #  if not valied return error details
        else:
            print(serialized_data.errors)
            print("not valied")
            return Response({"error":serialized_data.errors}, status=400)  
            


# user details
class user_details(APIView):
    
    def get(self, request, format = None):
        """
        this view is returning the user details who is authenticated
        """
        pass


class check(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print(request.auth)
        print(request.user)
        return Response({"check":"check_success"})  

    