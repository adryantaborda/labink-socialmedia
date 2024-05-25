from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import User
from .forms import MyUserCreationForm
import requests

# Create your views here.

def home(request):
    if request.user.is_authenticated == False:
        return render(request,'home.html')

def loginUser(request):
    
    if request.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        try:
            user = authenticate(username=username,password=password)
            user.save()
        except:
            messages.error(request,"Couldn't create your account")

    login(user)

    return render(request,'loginpage.html')


