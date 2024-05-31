from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class genders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
    
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=6,choices=genders.choices,default=None,null=True)
    birthday = models.DateField(null=True)

    USERNAME_FIELD = 'username'