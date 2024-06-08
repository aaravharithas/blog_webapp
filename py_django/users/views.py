from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
# Create your views here.

def register(request):
    if  request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Account is created for {username}! Now you can log In")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


@login_required
def profile(request):
    if  request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if  u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Profile hase been upadated for {u_form.instance.username}")
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {"u_form": u_form, "p_form": p_form}
    return render(request,'users/profile.html',context)

# check this code from here where I tried to send login successful message to home page after login.
# https://stackoverflow.com/questions/65893783/how-can-you-output-something-when-login-is-completed-django
# use this link as reffernce for this task

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = authenticate(request, username=username, password=password)
        except:
            messages.error(request, "User Not Found....")
            return redirect("users/login")

        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                first_name = request.user.first_name
                last_name = request.user.last_name
                messages.success(request, f'{first_name + " " + last_name} is logged in as {username}')
            return redirect("blog-home")
        else:
            messages.error(request, "Username or Password does not match...")

    return render(request, "users/login.html")