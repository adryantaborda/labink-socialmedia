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

                if request.POST.get("firstname"):
                    try:
                        firstname = request.POST.get("firstname")
                        user.first_name = firstname
                    except Exception as e:
                        print(e)

                if request.POST.get("lastname"):
                    try:
                        lastname = request.POST.get("lastname")
                        user.last_name = lastname
                    except Exception as e:
                        print(e)

                birthday = form.cleaned_data.get('birthday')
                if birthday:
                    user.set_birthday_clean(birthday.year, birthday.month, birthday.day)       
                    
                try:
                    user.save()
                    messages.success(request,'Congratulations! Your account was created!')
                    messages.success(request,'Please login')
                    
                    return redirect('home')
                except Exception as e:
                    print(e)
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
def userProfile(request,username):
    logged_user = request.user
    user = get_object_or_404(User, username=username)
    user_age = user.get_age()
    user_requests_connections = None
    get_request_connections = None
    connection_with_this_user = False
    usercounter = 0

    ''' user connections part '''

    if logged_user != username:
        user_requests_connections = ConnectionRequest.objects.filter(sender=logged_user, status='pending')
    get_request_connections = ConnectionRequest.objects.filter(receiver=logged_user, status='pending')

    if get_request_connections.exists() and request.method == 'POST':
        action = request.POST.get("buttonrequest") 
        connection_request = get_request_connections.first()
        if action == "accept":
            new_connection = UserConnections.objects.create(firstuser=logged_user,seconduser=connection_request.sender)
            new_connection.define_connection()

            new_connection.save()
            messages.success(request,f"@{connection_request.sender} is now connected with you")
            connection_request.delete()
        else:
            connection_request.delete()

    connections = list(UserConnections.objects.values_list("connection",flat=True))

    for connection in connections:
        if user.username in connection:
            usercounter += 1
            if logged_user != username and logged_user.username in connection:
                connection_with_this_user = True
    
    context = {'user':user,'logged_user':logged_user,'user_age':user_age,
               'get_request_connections':get_request_connections,
               'user_requests_connections':user_requests_connections,
               'connections':connections,'usercounter':usercounter,
               'connection_with_this_user':connection_with_this_user,}

    return render(request,'profile.html',context)






def requestConnection(request,username):
    try:
        receiver = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    sender = request.user
    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver,status='pending'):
        pass
    ConnectionRequest.objects.create(sender=sender,receiver=receiver,status='pending')

    return render(request,'requestconnection.html')

def cancelConnectionRequest(request,username):
    page = 'cancelConnectionRequest'
    sender = request.user
    try:
        receiver = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver):
        doRequest = ConnectionRequest.objects.get(sender=sender,receiver=receiver)
        doRequest.delete()

    return render(request,'cancelconnectionrequest.html',{'page':page})


def Connections(request,username):
    logged_user = request.user
    user = get_object_or_404(User, username=username)
    list_connections = list(UserConnections.objects.values_list("connection",flat=True))
    user_connections = []
    for connection in list_connections:
        if user.username in connection:
            print(connection)
            part1, part2 = connection.split("-")
            if user.username != part1:
                user_connections.append(part1) 
            else:
                user_connections.append(part2)
    print(user_connections)

    context = {'user':user,'logged_user':logged_user,'user_connections':user_connections}
         
    return render(request,'connections.html',context)

def cancelConnection(request,username):
    page = 'cancelConnection'
    logged_user = request.user
    user = get_object_or_404(User,username=username)

    list_connections = list(UserConnections.objects.values_list("connection",flat=True))

    if logged_user.username != user.username:
        for connection in list_connections:
            if user.username in connection and logged_user.username in connection:
                connectiontodelete = UserConnections.objects.filter(connection=connection)
                connectiontodelete.delete()
        
    return render(request,'cancelconnectionrequest.html',{'page':page})
