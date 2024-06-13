from django.contrib import admin
from .models import User 
from django.contrib.auth.admin import UserAdmin
from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(User,MyModelAdmin)



# Register your models here.
