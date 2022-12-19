from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegistration, UserEditForm
from .models import UserModel, GroupAdmin
from recognitions.models import RecognitionManagerModel
from attendance.models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
import datetime
from datetime import timedelta
import time

# Create your views here.
def user_present(user_id):
    date = datetime.datetime.now()
    user_last_login = UserModel.objects.get(pk = user_id).last_login + timedelta(hours = 2)
    user_last_login_date = user_last_login.strftime('%y-%m-%d')
    user_last_login_time = user_last_login.strftime('%H')
    current_date = date.strftime('%y-%m-%d')
    current_time = date.strftime('%H')

    if (user_last_login_date == current_date and int(current_time)- int(user_last_login_time) <2):
        return True
    else:
        return False

@login_required(login_url='/login/')
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
        week_roles = WeekAttendanceRoleManager.objects.get(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = current_week)
            )
        this_group_admin = GroupAdmin.objects.get(group = UserModel.objects.get(id = request.user.id).groups.first()).admin

        next_week_roles = WeekAttendanceRoleManager.objects.get(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = str(int(current_week)+1))
            )
        message = ""
        if request.POST.get('action') == 'change_leader':
            if user_present(week_roles.wor_leader.pk):
                message = "wor_leader"
            else:
                if user_present(week_roles.wor_engager.pk) and request.user == week_roles.wor_engager:
                    next_week_roles.wor_leader = week_roles.wor_leader
                    next_week_roles.save()
                    week_roles.wor_leader = week_roles.wor_engager
                    week_roles.save()
                    message = "wor_engager"
                else:
                    this_week_leader = week_roles.wor_leader
                    week_roles.wor_leader = request.user
                    week_roles_list = WeekAttendanceRoleManager.objects.filter( users_group = UserModel.objects.get(id = request.user.id).groups.first())
                    for week in week_roles_list:
                        if week.week_id.week_number > int(current_week):
                            if request.user == week.wor_leader:
                                week.wor_leader = this_week_leader
                                week.save()
                                break
                    week_roles.save()
            context = {
                "wor_leader_peresent": user_present(week_roles.wor_leader.pk),
                "wor_engager_peresent": user_present(week_roles.wor_engager.pk), 
                "message" : message,
                "week_role": week_roles,
                "next_week_role": next_week_roles
            }
            return render(request, 'account/agenda-facilitators.html', context=context)

        context = {
            "wor_leader_peresent": user_present(week_roles.wor_leader.pk),
            "wor_engager_peresent": user_present(week_roles.wor_engager.pk), 
            "message" : message,
            "week_role": week_roles,
            "next_week_role": next_week_roles
        }
        return render(request, 'account/agenda.html', context=context)
    else:
        return redirect("/login/")

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@permission_required('Can view session')
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
            try:
                wor_leader_update_week = wor_leader_update_list['week'].split(',')
            except:
                wor_leader_update_week = ""
            try:
                wor_leader_update_id = wor_leader_update_list['user_id'].split(',')
            except:    
                wor_leader_update_id =""

            for i in range(len(wor_leader_update_id)):
                try:
                    week_for_update = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = wor_leader_update_week[i]))
                    week_for_update.wor_leader = UserModel.objects.get(pk = int(wor_leader_update_id[i]))
                    week_for_update.save()
                except:
                    pass
            
            try:
                wor_engager_update_week = wor_engager_update_list['week'].split(',')
            except:
                wor_engager_update_week = ""
            try:
                wor_engager_update_id = wor_engager_update_list['user_id'].split(',')
            except:    
                wor_engager_update_id =""
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
