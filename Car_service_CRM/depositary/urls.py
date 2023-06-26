from django.urls import path
from . import views


urlpatterns = [
    path('', views.depositary, name='depositary'),
    path('add-part/', views.add_part, name='add-part'),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('edit-detail/<str:pk>/', views.edit_detail, name='edit-detail'),
    path('delete-detail/<str:pk>/', views.delete_detail, name='delete-detail'),
    path('owner-of-detail/<str:pk>/', views.owner_of_detail, name='owner-of-detail'),
    path('remove-detail-from-order/<str:pk>/', views.remove_detail_from_order, name='remove-detail-from_order'),
    path('add-detail/(<str:pk>, <str:sk>)/', views.add_detail, name='add-detail'),
    path('open-order/<str:pk>/', views.open_order, name='open-order'),
]