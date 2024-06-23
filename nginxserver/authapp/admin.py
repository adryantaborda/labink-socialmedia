from django.contrib import admin
from .models import User, ConnectionRequest, UserConnections
from django.contrib.auth.admin import UserAdmin
from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(User,MyModelAdmin)
admin.site.register(ConnectionRequest)
admin.site.register(UserConnections)


# Register your models here.
