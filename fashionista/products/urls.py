
from django.urls import path
from .views import ProductListView, ProductDetailSlugView, CreateSupplier, CreateProduct, UpdateProduct

urlpatterns = [
    path('',ProductListView.as_view(), name = 'productlist'),
    path('createsuppler/',CreateSupplier.as_view(),name = 'createsuppler'),
    path('createproduct/',CreateProduct.as_view(),name = 'createproduct'),
    path('updateproduct/<slug:slug>',UpdateProduct.as_view(),name = 'updateproduct'),
    path('details/<slug:slug>',ProductDetailSlugView.as_view(), name='productdetails'),
]


