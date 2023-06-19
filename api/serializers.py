from rest_framework import routers, serializers, viewsets
from .models import tasks, CustomUser

class task_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = tasks
        fields = ['email', 'task', 'task_details', 'task_due_date', 'task_due_time']



class user_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'contact_number', 'first_name', 'password']


class login_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
