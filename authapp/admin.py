from django.contrib import admin
from .models import User, ConnectionRequest, UserConnections
from django.contrib.auth.admin import UserAdmin

admin.site.register(User,admin.ModelAdmin)
admin.site.register(ConnectionRequest)
admin.site.register(UserConnections)


# Register your models here.
