from django.urls import path
from . import views

urlpatterns =[
    path('register_user/', views.register_user, name='register_user'),
    path('', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name="logoutuser"),
]