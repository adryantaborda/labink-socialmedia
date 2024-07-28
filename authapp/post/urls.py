from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<str:username>/post_id=<str:id>',views.postView,name="postview"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)