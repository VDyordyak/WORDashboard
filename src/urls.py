from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static
from src import settings

urlpatterns = [
    path('', include('authapp.urls', namespace='authapp')),
    path('admin/', admin.site.urls),
    path('actions/', include(('actions.urls', 'actions'), namespace='actions')),
    path('attendance/', include(('attendance.urls', 'recognition_page'), namespace='attendance')),
    path('improvements/', include(('improvements.urls', 'improvements'), namespace='improvements')),
    path('notice-board/', include(('notice_board.urls', 'notice_board'), namespace='notice-board')),
    path('recognitions/', include(('recognitions.urls', 'recognition_page'), namespace='recognitions')),
    path('she/', include(('she.urls', 'she_page'), namespace='she')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
