import time
import json
from tokenize import group 
from django.shortcuts import render, redirect
from .models import ActionTaskManagerModel
from authapp.models import UserModel
from django.http import JsonResponse
from django.http import HttpResponseRedirect
# Create your views here.


from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def actions(request):
    action_list = ActionTaskManagerModel.objects.all()
    user_profile_list = UserModel.objects.all()
    action_number = ActionTaskManagerModel.objects.filter(action_group =  UserModel.objects.get(id = request.user.id).groups.first()).count()
    response_data = {}
    group_members_count =  UserModel.objects.filter(groups =  UserModel.objects.get(id = request.user.id).groups.first()).count()
    
    if request.method == "GET" and request.GET.get('action') == 'get_data':
        action_pk = request.GET.get("action_pk", 1)
        selected_action = ActionTaskManagerModel.objects.get(id = action_pk)
        
        response_data['action_pk'] = action_pk
        response_data['issue_name'] = selected_action.issue_name
        response_data['action_text'] = selected_action.action_text
        response_data['solution_text'] = selected_action.solution_text
        response_data['action_status'] = selected_action.action_status
        response_data['assigned_users'] = selected_action.get_assigned_user()
        response_data['deadline_date'] = selected_action.deadline_date

        return JsonResponse(response_data)

    if request.POST.get('action') == 'add':
        selected_status= request.POST.get('selected_status')
        deadline_date = request.POST.get('deadline_date')
        issue_name = request.POST.get('issue_name')
        action_text = request.POST.get('action_text')
        solution_text = request.POST.get('solution_text')
        assigned_user_list = request.POST.get('assigned_user')
        assigned_user = assigned_user_list.split(',')

        response_data['issue_name'] = issue_name
        response_data['action_text'] = action_text
        response_data['solution_text'] = solution_text
        response_data['action_status'] = issue_name
        response_data['creation_date'] = selected_status
        response_data['assigned_user'] = assigned_user
        response_data['deadline_date'] = deadline_date
        
        new_action = ActionTaskManagerModel.objects.create(
                issue_name = issue_name,
                action_text = action_text,
                solution_text = solution_text,            
                deadline_date = deadline_date,
                action_status = selected_status,
            )
        for user in assigned_user:
            new_action.assigned_user.add(user)

    if request.POST.get('action') == 'edit':
        instance = ActionTaskManagerModel.objects.get(id=request.POST.get('action_pk'))
        selected_status = request.POST.get('selected_status')
        deadline_date = request.POST.get('deadline_date')
        issue_name = request.POST.get('issue_name')
        action_text = request.POST.get('action_text')
        solution_text = request.POST.get('solution_text')

        instance.issue_name=issue_name
        instance.action_text=action_text
        instance.solution_text=solution_text
        instance.action_status=selected_status
        instance.deadline_date=deadline_date
        
        #Connecting user with action
        assigned_user_list = request.POST.get('assigned_user')
        assigned_user = assigned_user_list.split(',')
        try:
            for user in assigned_user:
                instance.assigned_user.add(user)
        except:
            changed = False
        #Removing user from action connections
        unassigned_user_list = request.POST.get('unassigned_user')
        if unassigned_user_list != "":
            unassigned_user = unassigned_user_list.split(',')
            try:
                for user in unassigned_user:
                    instance.assigned_user.remove(user)
            except:
                changed = False
        instance.save()

    return render(request, 'actions_main.html', {
        'actions': action_list, 
        'user_profile_list': user_profile_list , 
        'group_members': group_members_count,
        'action_number': action_number
        })