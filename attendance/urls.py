from django.urls import path
from attendance.views import attendance, attendance_archive,change_user_status


urlpatterns = [
    path('', attendance, name='attendance_page'),
    path('status/<int:pk>', change_user_status, name='status_change'),
    path('archive/', attendance_archive, name='archive')
]

