from django.conf.urls.static import static
from src import settings
from django.urls import path, include
from .views import actions

urlpatterns = [
    path('', actions, name='action_main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
