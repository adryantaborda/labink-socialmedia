from django.contrib import admin
from .models import User, ConnectionRequest, UserConnections,Post, PostMessage
from django.contrib.auth.admin import UserAdmin

admin.site.register(User,admin.ModelAdmin)
admin.site.register(ConnectionRequest)
admin.site.register(UserConnections)
admin.site.register(Post)
admin.site.register(PostMessage)


# Register your models here.
