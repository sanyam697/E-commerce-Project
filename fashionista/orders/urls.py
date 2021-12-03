from django.urls import path
from . import views
urlpatterns=[
    path('orderlist',views.OrderList.as_view(),name='orderlist'),
    path('orderlist/orderdetails/<int:pk>',views.OrderDetails.as_view(),name='orderdetails'),
    path('orders/orderupdate/<int:pk>',views.UpdateOrder.as_view(),name='updateorder'),
]