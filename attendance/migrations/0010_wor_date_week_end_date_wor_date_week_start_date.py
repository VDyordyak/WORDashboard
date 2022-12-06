# Generated by Django 4.1.3 on 2022-12-05 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_remove_wor_date_wor_engager_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wor_date',
            name='week_end_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, verbose_name='week end date'),
        ),
        migrations.AddField(
            model_name='wor_date',
            name='week_start_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, verbose_name='week start date'),
        ),
    ]