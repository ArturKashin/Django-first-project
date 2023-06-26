from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns =[
    path('register_user/', views.register_user, name='register_user'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('view-workers/', views.view_workers, name='view-workers'),
    path('view-worker/<str:pk>/', views.view_worker, name='view-worker'),
    path('view-master/<str:pk>/', views.view_master, name='view-master'),
    path('api/', include(router.urls)),
]