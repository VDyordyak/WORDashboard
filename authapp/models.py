from datetime import datetime  
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.


class UserModel(AbstractUser):
    id = models.AutoField(primary_key=True)
    objects = UserManager()
    user_image = models.ImageField(blank=True, upload_to="profile_image/", default='profile_image/default_user_image.png',
                                   verbose_name="Profile image")
    user_position = models.CharField(blank=True, max_length=255, verbose_name="User position")
    user_about = models.TextField(blank=True, verbose_name="About you")