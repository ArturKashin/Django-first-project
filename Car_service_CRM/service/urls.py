from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('orders/', views.index, name='index'),
    path('worksorder/<str:pk>/', views.worksorder, name='worksorder'),
    path('', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('closed-orders/', views.closer_orders, name="closed_orders"),
    path('worksorder/delete-work/<str:pk>', views.delete_work, name="delete-work"),
    path('worksorder/at-work/<str:pk>', views.at_work, name='at-work'),
    path('worksorder/edit-work/<str:pk>', views.edit_work, name='edit-work')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)