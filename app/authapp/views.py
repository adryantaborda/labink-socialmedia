from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from .models import User, ConnectionRequest, UserConnections, Post, PostMessage
from .forms import MyUserCreationForm, PostForm, PostMessageForm
from .functions import check_strength, clean_username
import requests
import calendar
from datetime import date

# Create your views here.

'''Main Page'''

def home(request):
    user = request.user
    search_page = False
    friends_list = []
    all_founds = ''
    # Check if user is authenticated or not
    if request.user.is_authenticated == False:
        return redirect('login')
    
    # Search for user system
    if request.method == 'POST':
        search_page = True
        
        q = request.POST.get("_!username").lower() if request.POST.get("_!username") != None else ''
        if request.POST.get("_!username") == '':
            return redirect('home')
        all_founds = User.objects.filter(Q(name__icontains=q) |
                                         Q(username__icontains=q)
                                         )
        
        list_connections = list(UserConnections.objects.values_list("connection",flat=True))
        for connection in list_connections:
            for usr in all_founds:
                if usr.username in connection and user.username in connection:
                    friends_list.append(usr.username)

    #View Posts
    posts = Post.objects.all()
    
    # THIS IS IN TEST...
    
    # =------------------------
    

    return render(request,'home.html',{'search_page':search_page,'all_founds':all_founds,
                                       'friends_list':friends_list,'posts':posts,
                                       })      


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

# HERE YOU CAN CREATE AN USER ACCOUNT 

def createrUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = MyUserCreationForm()
    page = 'main'
    
    # VERIFY IF THE USER TRIED TO CREATE ITS ACCOUNT

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            data_username = form.cleaned_data.get('username')
            
            user.username = clean_username(data_username)

            birthday = form.cleaned_data.get('birthday')
            if birthday:
                user.set_birthday_clean(birthday.year, birthday.month, birthday.day)       
                
            try:
                user.save()
                
            except Exception as e:
                print(e)
                messages.error(request,"Couldn't create your account")

        else:
            messages.error(request,"Couldn't create your account. Invalid form")

    context = {'form':form,}    

    return render(request,'signuppage.html',context)


def logoutUser(request):
    # Just verify if the user is logged to logout
    # If not, you can't logout. You go back to main page
    if request.user.is_authenticated == False:
        return redirect('home')
    
    logout(request)
    return redirect('login')

'''See your profile'''

@login_required(login_url='login')
# Here you can check your user profile w
def userProfile(request,username):
    logged_user = request.user
    user = get_object_or_404(User, username=username)
    user_age = user.get_age()
    user_requests_connections = None
    get_request_connections = None
    connection_with_this_user = False
    usercounter = 0

    ''' user connections '''

    if logged_user != username:
        user_requests_connections = ConnectionRequest.objects.filter(sender=logged_user,receiver=user)
    get_request_connections = ConnectionRequest.objects.filter(receiver=logged_user)

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
    
    receiver = User.objects.get(username=username)
    sender = request.user

    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver,status='pending'):
        pass
    ConnectionRequest.objects.create(sender=sender,receiver=receiver,status='pending')

    return redirect(reverse('profile', kwargs={'username':receiver.username}))

def cancelConnectionRequest(request,username):
    sender = request.user
    try:
        receiver = User.objects.get(username=username)
    except:
        messages.error("Username not found.")

    if ConnectionRequest.objects.filter(sender=sender,receiver=receiver):
        doRequest = ConnectionRequest.objects.get(sender=sender,receiver=receiver)
        doRequest.delete()

    return redirect(reverse('profile', kwargs={'username':receiver.username}))

def Connections(request,username):
    logged_user = request.user
    userconnection_info = []
    user = get_object_or_404(User, username=username)
    list_connections = list(UserConnections.objects.values_list("connection",flat=True))
    
    for connection in list_connections:
        if user.username in connection:
            print(connection)
            part1, part2 = connection.split("-")
            if user.username != part1:
                
                userconnection_info = User.objects.filter(username=part1)
            else:
                userconnection_info = User.objects.filter(username=part2)
    
    print(userconnection_info)
    context = {'user':user,'logged_user':logged_user,
               'userconnection_info':userconnection_info}
         
    return render(request,'connections.html',context)

def cancelConnection(request,username):
    logged_user = request.user
    user = get_object_or_404(User,username=username)

    list_connections = list(UserConnections.objects.values_list("connection",flat=True))

    if logged_user.username != user.username:
        for connection in list_connections:
            if user.username in connection and logged_user.username in connection:
                connectiontodelete = UserConnections.objects.filter(connection=connection)
                connectiontodelete.delete()
        
    return redirect(reverse('profile', kwargs={'username':logged_user.username}))

# HERE YOU CAN CREATE YOUR OWN POSTS USING TEXT AND/OR IMAGES. 
# POSTING VIDEOS MAY BE ADDED LATER.

def createPost(request):
    user = request.user
    post_instance = None  # Assuming this is to create a new post, no initial instance
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        print(f"request.FILES: {request.FILES}")
        
        if form.is_valid():
            txt_content = form.cleaned_data.get('txt_content') 
            image = form.cleaned_data.get('image')
            
            if txt_content == None and image == None:
                messages.error(request, "You cannot create a blank post.")
            else:
                post = form.save(commit=False)
                post.post_user = request.user
                
                if image:
                    print(f"Image field populated: {image}")
                    post.image = image
                else:
                    print("Image field is not populated.")

                try:
                    post.save()
                    return redirect('home')
                except Exception as e:
                    messages.error(request, f"Could not create post. Please try again. Error: {e}")
        else:
            messages.error(request, "Incorrect information. Please try again.")
    else:
        form = PostForm(instance=post_instance)
    
    return render(request, 'postcreator.html', {'form': form})

# def CreatePostMessage(request,postid):
#     user = request.user
#     post = Post.objects.filter(id=postid)
#     form = PostMessage()
#     if request.method == "POST":
#         form = PostMessage(request.POST)
#         if form.is_valid():
#             try:
#                 message_text = request.POST.get('message_text')
#                 message = PostMessage.objects.create(message_creator=user,message_text=message_text,
#                                                     post_foreign_key=post)
#             except Exception as e:
#                 print(e)

#         else:
#             messages.error(request, "Some error has occurred. Please try again.")

#     return render(request, '.html', {'form': form, 'message':message})
            