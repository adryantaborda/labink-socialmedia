from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import User
from .forms import MyUserCreationForm
from .functions import check_strength, clean_username
import requests
import calendar
from datetime import date

# Create your views here.

'''Main Page'''

def home(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    return render(request,'home.html')      

'''Login user with username and password'''

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

'''Create your account'''

def createrUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            

            password = form.cleaned_data.get('password1')
            strong, message = check_strength(password)

            if strong:
                user = form.save(commit=False)
                
                data_username = form.cleaned_data.get('username')
                
                user.username = clean_username(data_username)

                birthday = form.cleaned_data.get('birthday')
                if birthday:
                    user.set_birthday_clean(birthday.year, birthday.month, birthday.day)       

                try:
                    user.save()
                    messages.success(request,'Congratulations! Your account was created!')
                    messages.success(request,'Please login')
                    
                    return redirect('home')
                except Exception as e:
                    messages.error(request,"Couldn't create your account")
            else:
                messages.error(request, message)

        else:
            
            print(form.data)
            messages.error(request,"Couldn't create your account. Invalid form")

    context = {'form':form,}    

    return render(request,'signuppage.html',context)
        
'''Logout of your account'''

def logoutUser(request):
    if request.user.is_authenticated == False:
        return redirect('home')
    
    logout(request)
    return redirect('login')

'''See your profile'''

@login_required(login_url='login')
def UserProfile(request,username):
    logged_user = request.user
    
    try:
        user = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    user_age = user.get_age()

    context = {'user':user,'logged_user':logged_user,'user_age':user_age}
    
    return render(request,'profile.html',context)

    