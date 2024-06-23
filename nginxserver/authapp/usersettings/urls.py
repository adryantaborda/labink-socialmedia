from . import views
from django.urls import path

urlpatterns = [
    path('profile',views.ProfileSettings,name='profile-edit'),
]
