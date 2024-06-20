from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import User, ConnectionRequest, UserConnections
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
    user = get_object_or_404(User, username=username)
    user_age = user.get_age()
    user_requests_connections = None
    get_request_connections = None
    
    if logged_user != username:
        user_requests_connections = ConnectionRequest.objects.filter(sender=logged_user, status='pending')
    get_request_connections = ConnectionRequest.objects.filter(receiver=logged_user, status='pending')


    if get_request_connections.exists() and request.method == 'POST':
        action = request.POST.get("buttonrequest") 
        connection_request = get_request_connections.first()
        if action == "accept":
            new_connection = UserConnections.objects.create(firstuser=logged_user,seconduser=connection_request.sender)
            new_connection.define_connection()
            print(new_connection.connection)
            messages.success(request,f"@{connection_request.sender} is now connected with you")
            connection_request.delete()
        else:
            connection_request.delete()
    

    context = {'user':user,'logged_user':logged_user,'user_age':user_age,
               'get_request_connections':get_request_connections,
               'user_requests_connections':user_requests_connections,}

    return render(request,'profile.html',context)

def RequestConnection(request,username):
    try:
        receiver = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    sender = request.user
    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver,status='pending'):
        pass

    ConnectionRequest.objects.create(sender=sender,receiver=receiver,status='pending')

    return render(request,'requestconnection.html')

def CancelConnection(request,username):
    sender = request.user
    try:
        receiver = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver):
        doRequest = ConnectionRequest.objects.get(sender=sender,receiver=receiver)
        doRequest.delete()

    return render(request,'deleteconnection.html')