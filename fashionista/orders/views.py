import datetime

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.utils import timezone

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

Order=apps.get_model('orders','Order')

class OrderList(LoginRequiredMixin,ListView):
    template_name = 'orders/orderlist.html'
    model = Order
    context_object_name = 'order'
    ordering = ['-updated']
    queryset = Order.objects.filter(confirm=True)

    def post(self, request, *args, **kwargs):
        object = self.get_object()

class OrderDetails(LoginRequiredMixin,DetailView):
    template_name = 'orders/orderdetails.html'
    model = Order
    context_object_name = 'order'


class UpdateOrder(LoginRequiredMixin,UpdateView):
    model = Order
    success_url = '/orders/orderlist'
    fields = ['status']
    template_name = 'orders/updateorderdetails.html'