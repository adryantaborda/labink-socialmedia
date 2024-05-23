from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    gender_options = ['MALE','FEMALE']
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    gender = models.CharField(choices=gender_options)
    birthday = models.DateField()

    def verify_gender():
        if User.gender not in User.gender_options:
            return 'Please, consider the specified genders.'