from django.forms import ModelForm
from .models import User, Post
from django.contrib.auth.forms import UserCreationForm
from django import forms   
from datetime import date
from django.contrib import auth 

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','gender','birthday']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = User 
        fields = ['name','bio','profile_picture']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_user','txt_content','image']
