# Generated by Django 4.1.3 on 2022-12-13 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recognitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recognitionmanagermodel',
            options={'ordering': ['user_profile']},
        ),
    ]
