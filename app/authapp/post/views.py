from django.shortcuts import render, redirect, get_object_or_404
from authapp.forms import ProfileForm
from django.urls import reverse
from authapp.models import User, Post, user_directory_path

# Create your views here.

def postView(request,username,id):
    user = User.objects.get(username=username)  # Get a specific user
    user_posts = user.post_creator.get(id=id)
    
    return render(request,'post.html',{'user_posts':user_posts})