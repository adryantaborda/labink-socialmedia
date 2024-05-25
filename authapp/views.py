from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import requests
# Create your views here.

def home(request):
    return render(request,'home.html')

def loginUser(request):
    if request.method == 'POST':
        name = requests.POST.get('name')
        password = requests.POST.get('password')


