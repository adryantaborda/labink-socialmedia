from django.db import models
from django.contrib.auth.models import AbstractUser
from image_cropping import ImageRatioField, ImageCropField
from PIL import Image
from django.conf import settings
from datetime import date
import os
# Create your models here.

def user_directory_path(instance,filename):
    avatar_pic_name = f'user_{instance.id}/profile.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, avatar_pic_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)

    return avatar_pic_name


class User(AbstractUser):
    

    class Genders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    class AttractedToGenders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        BOTH = 'BOTH'


    username = models.CharField(max_length=20,unique=True)
    bio = models.CharField(null=True, max_length=140,blank=True)
    avatar = models.ImageField(upload_to=user_directory_path,default='avatardefault.png',blank=True,null=True)

    email = models.EmailField()
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=6,choices=Genders.choices,default=None,null=True,blank=True)

    birthday = models.DateField(null=True,blank=True)


    """INFORMATIONS ABOUT THE USER RELATED TO PREFERENCES AND ETC """
    
    attractedTo = models.CharField(max_length=6,choices=AttractedToGenders.choices,default=None,null=True,blank=True)

    """ FOLLOWING SYSTEM """

    connectionsUser = models.ManyToManyField(null=True,blank=True)

    def set_birthday_clean(self,year,month,day):
        self.year = year
        self.month = month
        self.day = day

        self.birthday = date(self.year,self.month,self.day)
    
    def get_age(self):
        age = date.today() - self.birthday
        age = round(age.days / 365.25)
        return age
    def save(self, *args, **kwargs):
        if not self.avatar and not self.pk:
            print('here')
            self.avatar == 'media/avatardefault.png'
  
        super().save(*args, **kwargs)  # Save instance first to ensure self.avatar has a path

        if self.avatar:

            try:
                pic = Image.open(self.avatar.path)
                pic = pic.resize((300, 300), Image.LANCZOS)

                if pic.mode in ('RGBA','P'):
                    pic = pic.convert('RGB')

                pic.save(self.avatar.path, format='JPEG')
                print(pic.size)
                print("Succed image converting operation")
            except Exception as e:
                print(e)
                pass
        
    USERNAME_FIELD = 'username'