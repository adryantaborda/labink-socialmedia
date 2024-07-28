from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile',views.ProfileSettings,name='profile-edit'),
    path('name',views.userNameInput,name='user-name-input'),
    # path('profile_picture',views.userNameInput,name='user-pfp-input'),
    # path('bio',views.userNameInput,name='user-bio-input'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)