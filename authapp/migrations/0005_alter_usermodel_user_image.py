# Generated by Django 4.1.1 on 2022-11-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_alter_usermodel_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_image',
            field=models.ImageField(blank=True, default='profile_image/default_user_image.png', upload_to='profile_image/', verbose_name='Profile image'),
        ),
    ]
