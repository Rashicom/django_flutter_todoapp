from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import task_serializer,  user_serializer, login_serializer, task_list_all_serializer, user_details_serializer
from .models import tasks, CustomUser
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import datetime
from django.db.models import Q

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
    
    permission_classes = [IsAuthenticated]
    serializer_class = user_details_serializer

    def get(self, request, format = None):
        """
        this view is returning the user details who is authenticated
        """
        # fetching user data
        user_details = CustomUser.objects.get(email = request.user)

        # serializing and returning the data
        serialized_data = self.serializer_class(user_details)
        return Response(serialized_data.data, status=200)



# updat task
class updatetask(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer

    def patch(self, request, format = None):
        """
        this view is updating the fields which the user is provided
        user can update multiple fieslds at the same time.
        """
        print("patch request")
        task_id = request.data.get('task_id')
        email = request.data.get('email')
        
        # if the task id not found or email missmatch return error message
        if task_id is None:
            return Response({"message": "task_id must be given"}, status=400)
        if email and str(email) != str(request.user):
            return Response({"message": "email does not match"}, status=400)

        # fetching task model object to update
        model_obj = tasks.objects.get(task_id = task_id)
        
        """
        inisializing serializer, task object is passed to the serializer to update
        saving the serializer makes a replace to the field which we provided in the 
        request.data
        """
        serialized_data = self.serializer_class(model_obj ,data=request.data, partial=True)

        # if the felds are validated succussfully, save the serializer
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(serialized_data.data, status=200)
        
        # if any exception found return it
        except Exception as e:
            print(e)
            return Response({"status":"field not updated"}, status=403)


# delete task
class deletetask(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id, format = None):
        """
        delete the data using the task_id
        """
        
        # find the data form the data base and delete if any record foud
        try:
            tasks.objects.get(task_id = task_id, email = request.user).delete()
            return Response({"message":"deleted"}, status=200)
        
        # id exception found
        except Exception as e:
            print(e)    
            return Response({"message":"task not found"}, status=404)

      
# check task_status
class task_check(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer

    def patch(self, request, task_id, format = None):
        """
        patch a perticlurlar quety in the database
        """
        # if the data foung in the dabase update an scheched
        try:
            task_instance = tasks.objects.get(task_id = task_id, email = request.user)
            task_instance.task_status = True
            task_instance.save()

            # initializing a serializer to send the updated data to the doctor
            serialized_data = self.serializer_class(task_instance)

            # returning with updated data
            return Response(serialized_data.data, status=200)
        
        except Exception as e:
            print(e)
            return Response({"message":"task not found"}, status=404)



# uncheck task
class task_uncheck(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer

    def patch(self, request, task_id, format = None):
        """
        patch a perticlurlar quety in the database
        """
        # if the data foung in the dabase update an scheched
        try:
            task_instance = tasks.objects.get(task_id = task_id, email = request.user)
            task_instance.task_status = False
            task_instance.save()

            # initializing a serializer to send the updated data to the doctor
            serialized_data = self.serializer_class(task_instance)

            # returning with updated data
            return Response(serialized_data.data, status=200)
        
        except Exception as e:
            print(e)
            return Response({"message":"task not found"}, status=404)


class task_filter(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = task_serializer
    
    def get(self, request, format = None):
        """
        this view is returning the filtered data from recieved date to recieved to date
        if the user not send the to date it takes today date as defult
        using status, user can decide which data is fetched. (checked, ucchecked, all)
        defaulltly status takes all
        """

        # fetching data from the query params
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date', datetime.date.today())
        status = request.query_params.get('status',"all")

        # from date is mandatory
        if not from_date:
            return Response({"message":"from date must be provided"}, status=400)
        
        # making complex query accoring to the provided status
        if status == "checked":
            complex_q_optional = Q(task_status = True)

        elif status == "unchecked":
            complex_q_optional = Q(task_status = False)

        else:
            complex_q_optional = False

        # compaigning complext queries
        complex_q = Q(task_initial_date__lte = to_date) & Q(task_initial_date__gte = from_date) & Q(email = request.user)

        # filtering data
        try:

            # filter data according to complex_q_optonal
            if complex_q_optional:
                filtered_data = tasks.objects.filter(complex_q & complex_q_optional)
            else: 
                filtered_data = tasks.objects.filter(complex_q)
            
            # serializing data and return respose
            serialized_filtered_data = self.serializer_class(filtered_data, many=True)
            return Response(serialized_filtered_data.data, status=200)
        
        except Exception as e:
            print(e)
            return Response({"exception":"true"})

        

# checking api
class check_api(APIView):

    def get(self, request, format=None):
        print(request.auth)
        print(request.user)
        return Response({"message":"Api call success"}) 


class check_tocken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        return Response({"message":"authentication success"})


    