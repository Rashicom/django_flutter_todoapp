from rest_framework import routers, serializers, viewsets
from .models import tasks

class task_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = tasks
        fields = ['email', 'task', 'task_details', 'task_due_date', 'task_due_time']
