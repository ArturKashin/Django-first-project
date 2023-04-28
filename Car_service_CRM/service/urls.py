from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers


routers = routers.DefaultRouter()
routers.register(r'order', views.OrderViewSet)
routers.register(r'works-order', views.WorksOrderViewSet)

urlpatterns = [
    path('api/', include(routers.urls)),

    path('orders/', views.index, name='index'),
    path('worksorder/<str:pk>/', views.worksorder, name='worksorder'),
    path('close-order/<str:pk>/', views.close_order, name='close-order'),

    # закрытые наряды и работы
    path('closed-orders/', views.closer_orders, name="closed_orders"),
    path('closed-works/<str:pk>', views.closed_works, name="closed-works"),

    # для механика
    path('order-for-mechanical/', views.order_for_mechanical, name='order-for-mechanical'),
    path('works-for-mechanical/<str:pk>', views.works_for_mechanical, name='works-for-mechanical'),

    # удаление наряда и работ
    path('worksorder/delete-order/<str:pk>', views.delete_order, name="delete-order"),
    path('worksorder/delete-work/<str:pk>', views.delete_work, name="delete-work"),

    path('worksorder/at-work/<str:pk>', views.at_work, name='at-work'),
    path('worksorder/edit-work/<str:pk>', views.edit_work, name='edit-work'),
    path('worksorder/executor-completed/<str:pk>', views.executor_completed, name="executor-completed")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)