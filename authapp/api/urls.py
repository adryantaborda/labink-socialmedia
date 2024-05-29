from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',views.getRoutes),
    path('users/',views.getUsers),
    path('users/<int:pk>',views.getUserPK),
    path('login/',views.loginUser),
    path('register/',views.postUser),
    path('delete/',views.deleteUser),
]

urlpatterns = format_suffix_patterns(urlpatterns)