from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.user_login.as_view()),
    path('logout/', views.user_logout.as_view()),
    path('signup/',views.user_signup.as_view(), name='signup'),
    path('task_list_all/', views.task_list_all.as_view(), name="task_list"),
    path('addtask/', views.addtask.as_view(), name='addtask'),
    path('check/', views.check.as_view(), name='check')
]