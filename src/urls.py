from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from src import settings

urlpatterns = [
    path('', include('authapp.urls', namespace='authapp')),
    path('improvements/', include(('improvements.urls', 'improvements'), namespace='improvements')),
    path('actions/', include(('actions.urls', 'actions'), namespace='actions')),
    path('recognitions/', include(('recognitions.urls', 'recognition_page'), namespace='recognitions')),
    path('attendance/', include(('attendance.urls', 'recognition_page'), namespace='attendance')),
    path('she/', include(('she.urls', 'she_page'), namespace='she')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
