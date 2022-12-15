from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserModel, GroupAdmin


admin.site.register(UserModel)
admin.site.register(GroupAdmin)