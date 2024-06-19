from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms   
from datetime import date

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
        fields = ['username','email','bio','avatar']

