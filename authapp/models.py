from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

class User(AbstractUser):
    class genders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
    
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=6,choices=genders.choices,default=None)
    birthday = models.DateField()

    def verify_gender():
        super().clean()
        if User.gender not in User.genders:
            raise ValidationError("Choice must be either 1 or 2.")
        return User.gender
        
    USERNAME_FIELD = 'username'