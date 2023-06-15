from django.urls import path,include
from . import views

urlpatterns = [
    path('task_list/', views.home.as_view() ,name="task_list"),
    path('addtask/', views.addtask.as_view(),name='addtask'),

]