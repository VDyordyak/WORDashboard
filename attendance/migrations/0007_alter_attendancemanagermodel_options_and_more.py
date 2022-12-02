# Generated by Django 4.1.3 on 2022-12-01 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_alter_wor_date_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendancemanagermodel',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='attendancemanagermodel',
            name='user_status',
            field=models.CharField(choices=[('present', 'PRESENT'), ('absent', 'ABSENT'), ('excused', 'EXCUSED'), ('on_vacation', 'ON_VACATION')], default='present', max_length=11),
        ),
    ]
