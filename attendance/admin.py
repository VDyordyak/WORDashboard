from django.contrib import admin
from .models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
# Register your models here.
admin.site.register(AttendanceManagerModel)
admin.site.register(WOR_date)
admin.site.register(WeekAttendanceRoleManager)