from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from authapp.models import UserModel
from .forms import ImprovementCreateForm
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required
def improvements(request):
    improvement_create_form = ImprovementCreateForm(request.POST)
    improvements_list = ImprovementsTaskManagerModel.objects.all()
    user_profile_images = UserModel.objects.all()
    response_data = {}

    if request.POST.get('action') == 'add':
        improvement_title = request.POST.get('title')
        improvement_description = request.POST.get('description')
        selected_status= request.POST.get('status')

        start_date = request.POST.get('start_date')
        deadline_date = request.POST.get('deadline_date')
        
        assigned_user_list = str(request.POST.get('assigned_users'))
        assigned_user = assigned_user_list.split(',')

        new_improvement = ImprovementsTaskManagerModel.objects.create(
                creation_date = datetime.datetime.now(),

                title = improvement_title,
                description  = improvement_description,
                status = selected_status, 

                start_date = start_date,
                deadline_date = deadline_date,
                group = UserModel.objects.get(id = request.user.id).groups.first()
            )
        for user in assigned_user:
            new_improvement.assigned_user.add(user)
    return render(request, 'improvements/templates/improvement.html', {'improvements': improvements_list, 'create_form': improvement_create_form, 'user_profile_list': user_profile_images})

def change_status(request, pk):
    item_id = request.POST.get("item")
    items = ImprovementsTaskManagerModel.objects.get(id=pk)
    changed = True
    if "to_do" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status="to_do")
        except:
            changed = False
    elif "in_progress" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status='in_progress')
        except:
            changed = False
    elif "review" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status='review')
        except:
            changed = False
    else:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status="done")
        except:
            changed = False
    if changed:
        updated_improvement = ImprovementsTaskManagerModel.objects.get(id=pk)
        updated_improvement.save()
    return redirect('/improvements')

def improvement_edit(request, pk):
    instance = ImprovementsTaskManagerModel.objects.get(id=pk)
    improvements_update_form = ImprovementCreateForm(request.POST or None, instance=instance)
    if improvements_update_form.is_valid():
        improvements_update_form.save()
        return redirect('/improvements')
    return render(request, 'improvements/templates/edit_improvement.html', {'update_form': improvements_update_form, })