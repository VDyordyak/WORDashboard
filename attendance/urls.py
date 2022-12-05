from django.urls import path
from attendance.views import attendance


urlpatterns = [
    path('', attendance, name='attendance_page'),
]

