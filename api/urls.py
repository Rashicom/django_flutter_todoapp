from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.user_login.as_view()),
    path('logout/', views.user_logout.as_view()),
    path('signup/',views.user_signup.as_view()),
    path('task_list_all/', views.task_list_all.as_view()),
    path('addtask/', views.addtask.as_view()),
    path('check/', views.check.as_view()),
    path('task_list_checked/', views.task_list_checked.as_view()),
    path('task_list_unchecked/', views.task_list_unchecked.as_view()),

]