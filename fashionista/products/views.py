from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormMixin

from django.views.generic.list import ListView


from .forms import SupplierForm, ProductForm, ItemForm
from .models import Product
Cart = apps.get_model('carts','Cart')

class ProductListView(ListView):
    template_name = 'products/productlist.html'
    queryset = Product.objects.all() #it returns object_list
    context_object_name = 'product' #object_list =product
    extra_context = {'title':'Product'}
    paginate_by = 6

class ProductDetailSlugView(FormMixin,DetailView):
    form_class = ItemForm
    template_name = 'products/productdetails.html'
    queryset = Product.objects.all() #it returns object
    context_object_name = 'product' # object==product

    extra_context = {'title':'Product Details'}
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailSlugView,self).get_context_data(**kwargs)
        cart ,_ = Cart.objects.new_or_get(request)
        context['cart']=cart
        return context


class CreateSupplier(LoginRequiredMixin,TemplateView):
    form = SupplierForm
    template_name = "products/createsupplier.html"
    extra_context = {'title': 'Create Supplier'}

    def get(self, request, *args, **kwargs):
        form=self.form()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request,self.template_name,{'form':form})

class CreateProduct(LoginRequiredMixin,CreateView):
    form = ProductForm
    template_name = "products/createproduct.html"
    extra_context = {'title': 'Create Product'}

    def get(self, request, *args, **kwargs):
        form=self.form()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("productlist")
        return render(request,self.template_name,{'form':form})

class UpdateProduct(LoginRequiredMixin,UpdateView):
    model = Product
    success_url = '/product/'
    fields = ['name','description','price','image','quantity','supplername']
    template_name = 'products/updateproduct.html'
    extra_context = {'title': 'Update Product'}