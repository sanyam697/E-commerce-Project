from django.urls import path
from . import views

urlpatterns=[
    path('download=<int:id>',views.generatepdf_view,name="invoice"),
]