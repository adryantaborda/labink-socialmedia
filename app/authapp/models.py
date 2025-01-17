from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from datetime import date
import os
# Create your models here.

''' GET INSTANCE ID AND PATH FOR PROFILE PICTURE STORAGE'''


def user_directory_path(instance,filename):
    profile_pic_name = f'user_{instance.id}/profile.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name

def user_directory_for_posts_image_path(instance,filename):
    post_image_name = f'user_{instance.post_user.id}/posts_image/{filename}'
    
    return post_image_name

''' USER MODEL '''

class User(AbstractUser):

    class Genders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    class AttractedToGenders(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'
        BOTH = 'BOTH'

    #MAIN INFOS
    name = models.CharField(max_length=40,null=True,blank=True)
    username = models.CharField(max_length=20,unique=True)
    bio = models.CharField(null=True, max_length=140,blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path,default='user_default/pfpdefault.png',blank=True,null=True)

    email = models.EmailField()
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=6,choices=Genders.choices,default=None,null=True,blank=True)

    birthday = models.DateField(null=True,blank=True)



    #INFORMATIONS ABOUT THE USER RELATED TO SOCIAL LIFE 
    
    attractedTo = models.CharField(max_length=6,choices=AttractedToGenders.choices,default=None,null=True,blank=True)

    #Post relationship

    #DEFINE YEAR, MONTH AND DAY AND SET YOUR BIRTHDAY 

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
        if not self.profile_picture and not self.pk:
            self.profile_picture == 'media/user_default/pfpdefault.png'
  
        super().save(*args, **kwargs)  # Save instance first to ensure self.profile_picture has a path

        #Due to the following code being inside save function, it will always resize the image when changes 
        #in the user profile are made. For this we have to mode this code to other separated function
        #Code will stay like this for now.
        if self.profile_picture:
            try:
                pic = Image.open(self.profile_picture.path)
                pic = pic.resize((300, 300), Image.LANCZOS)

                if pic.mode in ('RGBA','P'):
                    pic = pic.convert('RGB')

                pic.save(self.profile_picture.path, format='JPEG')
                print(pic.size)
                print("Succed image converting operation")
            except Exception as e:
                print(e)
                pass
        
    USERNAME_FIELD = 'username'

''' A REQUEST SEND BETWEEN USERS TO CREATE A CONNECTION '''

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='sender',related_name='sender_request')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='receiver',related_name='receiver_request')
    created_at = models.DateTimeField(auto_now_add=True)

''' DEFINE THE CONNECTION BETWEEN USERS '''
    
class UserConnections(models.Model):
    firstuser = models.ForeignKey(User,on_delete=models.CASCADE, related_name='first_user',default=None)
    seconduser = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='second_user',default=None)
    connection = models.CharField(max_length=300,default=None,blank=True,null=True)

    def define_connection(self):
        if self.firstuser and self.seconduser:
            self.connection  = f"{self.firstuser.username}-{self.seconduser.username}"

''' USERS POSTS '''

class Post(models.Model):
    post_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',default=None,blank=True,null=True)
    txt_content = models.CharField(max_length=5000,null=True,blank=True)
    image = models.ImageField(upload_to=user_directory_for_posts_image_path,null=True,blank=True)

class PostMessage(models.Model):
    message_text = models.CharField(max_length=400)
    message_creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='messages',default=None,blank=True,null=True)
    post_foreign_key = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='messages',default=None,blank=True,null=True)
