from django.shortcuts import render, redirect
from authapp.models import UserModel
from .models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
import datetime
import json

# Create your views here.
def attendance(request):
    week_list = WOR_date.objects.all()
    attendance_list = AttendanceManagerModel.objects.all()
    user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())

    current_week = datetime.datetime.now().strftime('%U')
    if current_week[0] == "0":
        current_week = int(current_week) % 10
    else:
        current_week = int(current_week) 

    if request.POST.get('action') == 'update':
        week_no= int(request.POST.get('current_week'))
        user_status_dictionary = json.loads(request.POST.get('user_status_dictionary'))

        for id in user_status_dictionary:
            try:
                new_attendance = AttendanceManagerModel.objects.get(date = WOR_date.objects.get(week_number = week_no), person = UserModel.objects.get(id = id))
                new_attendance.user_status = user_status_dictionary[id]
                new_attendance.save()
            except AttendanceManagerModel.DoesNotExist:
                new_attendance = AttendanceManagerModel.objects.create(
                    date = WOR_date.objects.get(week_number = week_no),
                    person = UserModel.objects.get(id = id),
                    user_status = user_status_dictionary[id],
                )
                new_attendance.save()
    week_roles = WeekAttendanceRoleManager.objects.all()
    return render(request, 'attendance.html', {
        'attendances': attendance_list, 
        'users': user_list, 
        'week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles
        })

