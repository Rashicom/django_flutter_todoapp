from rest_framework import routers, serializers, viewsets
from .models import tasks, CustomUser

class task_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = tasks
        fields = '__all__'


class user_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'contact_number', 'first_name', 'password']


class login_serializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required = True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


# task_list_all serializer
class task_list_all_serializer(serializers.ModelSerializer):

    """
    serializing all the data from the task table and 
    this used to render all the task info to the user
    """
    class Meta:
        model = tasks
        fields = '__all__'

# user details
class user_details_serializer(serializers.ModelSerializer):

    """
    serializer for user details
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'contact_number', 'first_name']

# update serializer
class update_serializer(serializers.ModelSerializer):

    class Meta:
        model = tasks
        fields = '__all__'

