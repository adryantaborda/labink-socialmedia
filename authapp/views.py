from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import User
from .forms import MyUserCreationForm
import requests

# Create your views here.

def home(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    return render(request,'home.html')      

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Couldn't create your account")

        authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
        
    return render(request,'loginpage.html',{'page':page})

def createrUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                messages.success(request,'Congratulations! Your account was created!')
                messages.success(request,'Please login')
                return redirect('home')
            except:
                messages.error(request,"Couldn't create your account")

    context = {'form':form}    

    return render(request,'signuppage.html',context)
        


