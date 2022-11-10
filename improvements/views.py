from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from authapp.models import UserModel
from .forms import ImprovementCreateForm

# Create your views here.
@login_required
def improvements(request):
    improvement_create_form = ImprovementCreateForm(request.POST)
    if improvement_create_form.is_valid():
        improvement_create_form.save()
        current_improvement = ImprovementsTaskManagerModel.objects.get(id=improvement_create_form.instance.pk)
        current_improvement.action_group = request.user.groups.get(id='1')
        current_improvement.save()
    improvements_list = ImprovementsTaskManagerModel.objects.all()
    user_profile_images = UserModel.objects.all()
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