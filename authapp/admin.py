from django.contrib import admin
from .models import User, ConnectionRequest, UserConnections
from django.contrib.auth.admin import UserAdmin

class MyModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(User,MyModelAdmin)
admin.site.register(ConnectionRequest)
admin.site.register(UserConnections)


# Register your models here.
