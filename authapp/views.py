from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm
from .models import UserModel
from recognitions.models import RecognitionManagerModel
from attendance.models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
import datetime
import time

# Create your views here.

@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    profile_information = UserModel.objects.get(id=request.user.pk)
    return render(request, 'authapp/dashboard.html', {
        'context': context, 
        'profile_information': profile_information, 
        'date_now': str(type(datetime.date(2022,1,1).strftime('%U'))),
        })
@login_required
def agenda(request):
    date = datetime.datetime.now()
    current_week = date.strftime('%U')
    week_roles = WeekAttendanceRoleManager.objects.filter(
        users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
        week_id = WOR_date.objects.get(week_number = current_week)
        )
    try:
        next_week_roles = WeekAttendanceRoleManager.objects.filter(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = str(int(current_week)+1))
            )
    except:
        next_week_roles = ""

    context = {
        "week_roles": week_roles,
        "next_week_roles": next_week_roles
    }
    return render(request, 'authapp/agenda.html', context=context)  


def wor_calendar_generation(request):
    current_group_user_list = UserModel.objects.filter(groups =  UserModel.objects.get(id = request.user.id).groups.first())
    date = datetime.datetime.now()

    for i in range(52):
        current_week = date.strftime('%U')
        start = date - datetime.timedelta(days=date.weekday())
        end = start + datetime.timedelta(days=6)
        if current_week[0] == "0":
            current_week = int(current_week) % 10
        else:
            current_week = current_week 

        WOR_date.objects.get_or_create(
            start_date = start,
            end_date = end,
            week_number = current_week,
        )
        date = date + datetime.timedelta(days=7)
    ready_selected =  current_group_user_list[0].id
    for week in WOR_date.objects.all():  
        for j in range(current_group_user_list.count()):
            if current_group_user_list[j].id == ready_selected:
                if current_group_user_list[j] == current_group_user_list[current_group_user_list.count()-1]:
                    WeekAttendanceRoleManager.objects.get_or_create(
                        week_id = WOR_date.objects.get(week_number = week.week_number),
                        users_group = UserModel.objects.get(id = request.user.id).groups.first(),
                        wor_leader = current_group_user_list[j],
                        wor_engager = current_group_user_list[0],
                    )
                    ready_selected =  current_group_user_list[0].id
                    break
                else:
                    WeekAttendanceRoleManager.objects.get_or_create(
                        week_id =  WOR_date.objects.get(week_number = week.week_number),
                        users_group = UserModel.objects.get(id = request.user.id).groups.first(),
                        wor_leader = current_group_user_list[j],
                        wor_engager = current_group_user_list[j+1],
                    )
                    ready_selected =  current_group_user_list[j+1].id
                    break  
    return redirect('/accounts/settings/')

def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            time.sleep(2)

            new_user.groups.add(UserModel.objects.get(id = request.user.id).groups.first())
            new_user.save()

            RecognitionManagerModel.objects.create(
                user_profile = UserModel.objects.get(id = new_user.id)
            )
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)

@login_required
def settings(request):
    if request.POST.get('action') == 'update':
            import json
            from django.http import JsonResponse
            responce = {}
            wor_leader_update_list =  request.POST.get('wor_leaders_list')   
            wor_engager_update_list = request.POST.get('wor_engagers_list')

            return JsonResponse(wor_leader_update_list)
    try:
        week_list = WOR_date.objects.all()
        user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())

        current_week = datetime.datetime.now().strftime('%U')
        if current_week[0] == "0":
            current_week = int(current_week) % 10
        else:
            current_week = int(current_week)

        week_roles = WeekAttendanceRoleManager.objects.all()
        current_week_roles = WeekAttendanceRoleManager.objects.filter(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = current_week)
            )
            
        return render(request, 'account/facilitator_settings.html', {
        'users': user_list, 
        'current_week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles,
        'current_week_roles': current_week_roles
        })
    except:
        return render(request, 'account/facilitator_settings.html')
