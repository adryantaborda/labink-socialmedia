from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from image_cropping import ImageCropWidget
from django import forms   

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','gender','birthday']

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','bio','avatar']
