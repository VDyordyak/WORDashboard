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

def agenda(request):
    if request.user.is_authenticated:
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
    else:
        redirect("login/")

@login_required
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
                    try:
                        WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = week.week_number))
                        WeekAttendanceRole.wor_leader = current_group_user_list[j]
                        WeekAttendanceRole.wor_engager = current_group_user_list[0]
                        WeekAttendanceRole.save()
                        ready_selected =  current_group_user_list[0].id
                        break
                    except:
                        WeekAttendanceRoleManager.objects.create(
                            week_id = WOR_date.objects.get(week_number = week.week_number),
                            users_group = UserModel.objects.get(id = request.user.id).groups.first(),
                            wor_leader = current_group_user_list[j],
                            wor_engager = current_group_user_list[0],
                        )
                        ready_selected =  current_group_user_list[0].id
                        break 
                else:
                    try:
                        WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = week.week_number))
                        WeekAttendanceRole.wor_leader = current_group_user_list[j]
                        WeekAttendanceRole.wor_engager = current_group_user_list[j+1]
                        WeekAttendanceRole.save()
                        ready_selected =  current_group_user_list[j+1].id
                        break
                    except:
                        WeekAttendanceRoleManager.objects.get_or_create(
                            week_id =  WOR_date.objects.get(week_number = week.week_number),
                            users_group = UserModel.objects.get(id = request.user.id).groups.first(),
                            wor_leader = current_group_user_list[j],
                            wor_engager = current_group_user_list[j+1],
                        )
                        ready_selected =  current_group_user_list[j+1].id
                        break
                      
    return redirect('/accounts/settings/')

@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            time.sleep(1)

            new_user.groups.add(UserModel.objects.get(id = request.user.id).groups.first())
            new_user.save()

            RecognitionManagerModel.objects.get_or_create(
                user_profile = UserModel.objects.get(id = new_user.id)
            )
            time.sleep(1)
            # updating the attendance table base on new user creation date
            date = datetime.datetime.now()
            current_week = WOR_date.objects.get(week_number = date.strftime('%U'))
            current_group_user_list = UserModel.objects.filter(groups =  UserModel.objects.get(id = request.user.id).groups.first())
            ready_selected = WeekAttendanceRoleManager.objects.get(week_id = current_week).wor_engager.id

            for week in WOR_date.objects.all():  
                if week.week_number <= current_week.week_number:
                    AttendanceManagerModel.objects.create(
                        date = WOR_date.objects.get(week_number = week.week_number),
                        person = UserModel.objects.get(id = new_user.id),
                        user_status = 'comes_later',
                    )
                for j in range(current_group_user_list.count()):
                    if week.week_number > current_week.week_number:
                        if current_group_user_list[j].id == ready_selected:
                            if current_group_user_list[j] == current_group_user_list[current_group_user_list.count()-1]:
                                WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = week.week_number))
                                WeekAttendanceRole.wor_leader = current_group_user_list[j]
                                WeekAttendanceRole.wor_engager = current_group_user_list[0]
                                WeekAttendanceRole.save()
                                ready_selected =  current_group_user_list[0].id
                                break
                            else:
                                WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = week.week_number))
                                WeekAttendanceRole.wor_leader = current_group_user_list[j]
                                WeekAttendanceRole.wor_engager = current_group_user_list[j+1]
                                WeekAttendanceRole.save()
                                ready_selected =  current_group_user_list[j+1].id
                                break
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
            wor_leader_update_list =  json.loads(request.POST.get('wor_leaders_list'))  
            wor_engager_update_list = json.loads(request.POST.get('wor_engagers_list'))
            responce ={
                "user_id":'',
                "week":''
            }
            wor_leader_update_week = wor_leader_update_list['week'].split(',')
            wor_leader_update_id = wor_leader_update_list['user_id'].split(',')

            for i in range(len(wor_leader_update_id)):
                try:
                    week_for_update = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = wor_leader_update_week[i]))
                    week_for_update.wor_leader = UserModel.objects.get(pk = int(wor_leader_update_id[i]))
                    week_for_update.save()
                except:
                    pass
            wor_engager_update_week = wor_engager_update_list['week'].split(',')
            wor_engager_update_id = wor_engager_update_list['user_id'].split(',')
            for i in range(len(wor_engager_update_id)):
                try:
                    week_for_update = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = wor_engager_update_week[i]))
                    week_for_update.wor_engager = UserModel.objects.get(pk = int(wor_engager_update_id[i]))
                    week_for_update.save()
                except:
                    pass

            return JsonResponse(responce)
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
