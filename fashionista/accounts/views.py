from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import VisitorEmail,Contact
from .forms import LoginForm, RegistrationForm, ContactForm,VisitorForm

Product=apps.get_model('products','Product')
def home(request):
    product=Product.objects.all()
    return render(request,template_name='home.html',context={'title':'Home','product':product})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                try:
                    del request.session['guest_visitor_id']
                except:
                    pass
                return redirect('/')
            else:
                return redirect('/login')

    return render(request, template_name='login.html', context={'title': 'Login', 'form':form,})


def visitor_view(request):
    form = VisitorForm(request.POST or None)
    next_ =request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path =next_ or next_post or None
    if form.is_valid():
        email =form.cleaned_data.get("email")
        new_visitor_email = VisitorEmail.objects.create(email=email)
        request.session['guest_visitor_id'] = new_visitor_email.email
        if is_safe_url(redirect_path,request.get_host()):
            print("Safe url")
            return redirect(redirect_path,request.get_host())
        else:
            return redirect("checkout_home")
    return redirect("checkout_home")


class RegisterView(LoginRequiredMixin,CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/login/'



def conatct_page(request):
    form = ContactForm(request.POST or None)
    context ={'form':form,"title":'Contact Form',}
    if request.method =="POST":
        if form.is_valid():
            fullname=form.cleaned_data['fullname']
            email=form.cleaned_data['email']
            content=form.cleaned_data['content']
            Contact.objects.create(fullname=fullname,email=email,content=content)
            context={'title':"Thank You",'data':"Thanks for message! we will get right back to you.",}

    return render(request,"accounts/contact.html",context)

@login_required
def account_view(request):
    return render(request,'accounts/account.html',{})

class ContactList(ListView):
    model = Contact
    template_name = 'accounts/receivedcontacts.html'
    context_object_name = 'contact'
    extra_context = {'title':'Recieved Contacts'}
