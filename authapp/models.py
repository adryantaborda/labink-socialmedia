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

    def clean(self):
        super().clean()
        self.verify_gender()


    def verify_gender():

        if User.gender not in User.genders:
            raise ValidationError("Invalid gender choice. Must be 'MALE' or 'FEMALE'")
        return User.gender
        
    USERNAME_FIELD = 'username'