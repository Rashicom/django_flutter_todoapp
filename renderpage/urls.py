from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home.as_view(), name="todopage"),
    path('login/', views.login.as_view(), name="loginpage"),
    path('signup/', views.signup.as_view(), name="signuppage")
]