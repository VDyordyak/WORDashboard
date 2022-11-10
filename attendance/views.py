from django.shortcuts import render, redirect
from authapp.models import UserModel
from .models import AttendanceManagerModel, WOR_date
import datetime

# Create your views here.
def attendance(request):
    week_list = WOR_date.objects.all()
    attendance_list = AttendanceManagerModel.objects.all()
    user_list = UserModel.objects.all()

    current_week = datetime.datetime.now().strftime('%U')
    if current_week[0] == "0":
        current_week = int(current_week) % 10
    else:
        current_week = int(current_week) 

    return render(request, 'attendance.html', {
        'attendances': attendance_list, 
        'users': user_list, 
        'week': current_week, 
        'week_list' :  week_list
        })

def change_user_status(request, pk):
    changed = True
    if "not_present" in request.POST:
        try:
            date = datetime.datetime.now()   
            current_week = date.strftime('%U')
            if current_week[0] == "0":
                current_week = int(current_week) % 10
            else:
                current_week = current_week 

            AttendanceManagerModel.objects.create(
                person = UserModel.objects.get(id=pk),
                user_status = 'not_present',
                date = WOR_date.objects.get(week_number = current_week)
            )
        except:
            changed = False
    elif "excused" in request.POST:
        try:
            date = datetime.datetime.now()   
            current_week = date.strftime('%U')
            if current_week[0] == "0":
                current_week = int(current_week) % 10
            else:
                current_week = current_week 

            AttendanceManagerModel.objects.create(
                person = UserModel.objects.get(id=pk),
                user_status = 'excused',
                date = WOR_date.objects.get(week_number = current_week)
            )
        except:
            changed = False
    else:
        try:
            date = datetime.datetime.now()   
            current_week = date.strftime('%U')
            if current_week[0] == "0":
                current_week = int(current_week) % 10
            else:
                current_week = current_week 

            AttendanceManagerModel.objects.create(
                person = UserModel.objects.get(id=pk),
                user_status = 'on_vacation',
                date = WOR_date.objects.get(week_number = current_week)
            )
        except:
            changed = False
    if changed:
        UserModel.objects.filter(id=pk).update(last_punch_week=current_week)
    return redirect('/attendance')

def attendance_archive(request):
    pass
