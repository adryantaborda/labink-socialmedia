from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginUser,name='login'),
    path('signup/',views.createrUser,name='signup'),
    path('logout/',views.logoutUser, name="logout"),
    path('<str:username>',views.userProfile, name="profile"),
    path('connecting/<str:username>',views.requestConnection, name="requestConnection"),
    path('cancel-connection-request/<str:username>',views.cancelConnectionRequest, name="cancelConnectionRequest"),
    path('disconnecting/<str:username>',views.cancelConnection,name='cancelConnection'),
    path('connections/<str:username>',views.Connections,name='connections')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)