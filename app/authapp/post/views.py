from django.shortcuts import render, redirect, get_object_or_404
from authapp.forms import ProfileForm, PostForm, PostMessageForm
from django.urls import reverse
from authapp.models import User, Post
from authapp.models import User, Post, PostMessage
from django.contrib import messages
# Create your views here.

def postView(request,username,id):
    message = ''
    user = User.objects.get(username=username) 
    logged_user = request.user
    user_posts = user.posts.get(id=id)
    user = request.user
    post = Post.objects.get(id=id)
    print(post)
    messages = post.messages.all()

    form = PostMessageForm()
    if request.method == "POST":
        form = PostMessageForm(request.POST)
        if form.is_valid():
            try:
                message_text = request.POST.get('message_text')
                message = PostMessage.objects.create(message_creator=logged_user,message_text=message_text,
                                                    post_foreign_key=post)
            except Exception as e:
                print(e)
        else:
            messages.error(request, "Some error has occurred. Please try again.")
    
    return render(request,'post.html',{'user_posts':user_posts,'form': form, 
                                       'message':message,'messages':messages})