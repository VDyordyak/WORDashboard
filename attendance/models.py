from datetime import datetime
import calendar
from django.db import models

# Create your models here.
from authapp.models import UserModel

# Create your models here.
class WOR_date (models.Model):
    wor_date = models.DateField(default=datetime.now, verbose_name="WOR date")
    week_number = models.IntegerField(default="0", verbose_name="Week")
    wor_leader = models.ForeignKey(UserModel, related_name='wor_leader', on_delete=models.CASCADE, verbose_name="WOR Learder")
    wor_engager = models.ForeignKey(UserModel, related_name='wor_engager', on_delete=models.CASCADE, verbose_name="WOR Engager")
    
    def __str__(self):
        return "week:"+str(self.week_number)+"; date:"+str(self.wor_date.day)+" of "+ calendar.month_name[self.wor_date.month]
    class Meta:
        ordering = ['week_number']
class AttendanceManagerModel(models.Model):
    USER_STATUS = (
        ('present', 'PRESENT'),
        ('absent', 'ABSENT'),
        ('excused', 'EXCUSED'),
        ('on_vacation', 'ON_VACATION')
    )
    date = models.ForeignKey(WOR_date, on_delete=models.CASCADE)
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=11, choices=USER_STATUS, default='present')

    def __str__(self):
        return self.person.username

    class Meta:
        ordering = ['date']
