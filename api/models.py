from django.db import models

# Create your models here.

class tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=50)
    task_details = models.TextField()
    task_initial_date = models.DateField(auto_now=False, auto_now_add=True)
    task_initial_time = models.TimeField(auto_now=False, auto_now_add=True)
    task_due_date = models.DateField(auto_now=False, auto_now_add=False)
    task_due_time = models.TimeField(auto_now=False, auto_now_add=False)


# {"task" :  "new task", "task_details" : "task_details new", "task_due_date": "26-06-2023", "task_due_time":"09:10"}
