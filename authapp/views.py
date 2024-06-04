from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import User
from .forms import MyUserCreationForm
from .functions import check_strength
import requests

# Create your views here.

def home(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    return render(request,'home.html')      

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Couldn't login")

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            
            return redirect('home')
        
    return render(request,'loginpage.html',{'page':page})

def createrUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():

            password = form.cleaned_data.get('password1')
            strong, message = check_strength(password)
            print(strong,message)

            if strong:
                user = form.save(commit=False)
                try:
                    user.save()
                    messages.success(request,'Congratulations! Your account was created!')
                    messages.success(request,'Please login')
                    return redirect('home')
                except:
                    messages.error(request,"Couldn't create your account")
            else:
                messages.error(request, message)
        else:
            messages.error(request,"Couldn't create your account")

    context = {'form':form}    

    return render(request,'signuppage.html',context)
        

def logoutUser(request):
    if request.user.is_authenticated == False:
        return redirect('home')
    
    logout(request)
    return redirect('login')
    