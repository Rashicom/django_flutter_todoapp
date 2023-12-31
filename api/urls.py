from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from . import views


urlpatterns = [
    path('signup/',views.user_signup.as_view()),
    path('login/',views.user_login.as_view()),
    path('logout/', views.user_logout.as_view()),
    path('task_list_all/', views.task_list_all.as_view()),
    path('addtask/', views.addtask.as_view()),
    path('check_api/', views.check_api.as_view()),
    path("check_tocken/", views.check_tocken.as_view()),
    path('task_list_checked/', views.task_list_checked.as_view()),
    path('task_list_unchecked/', views.task_list_unchecked.as_view()),
    path('user_details/', views.user_details.as_view()),
    path('updatetask/',views.updatetask.as_view()),
    path('deletetask/<int:task_id>', views.deletetask.as_view()),
    path('task_check/<int:task_id>', views.task_check.as_view()),
    path('task_uncheck/<int:task_id>', views.task_uncheck.as_view()),
    path('task_filter/', views.task_filter.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    

]   