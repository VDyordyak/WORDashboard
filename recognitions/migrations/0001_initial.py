# Generated by Django 4.1.3 on 2023-02-17 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecognitionManagerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiative_value', models.IntegerField(default='0', verbose_name='Initiative')),
                ('understand_value', models.IntegerField(default='0', verbose_name='Understanding Business Environment')),
                ('practice_value', models.IntegerField(default='0', verbose_name='Practice what you Preach')),
                ('result_focus_value', models.IntegerField(default='0', verbose_name='Result focus')),
                ('know_yourself_value', models.IntegerField(default='0', verbose_name='Know Yourself')),
                ('cooperation_value', models.IntegerField(default='0', verbose_name='Proactive Cooperation')),
                ('total_stars', models.IntegerField(default='0', verbose_name='Total stars')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user_profile'],
            },
        ),
    ]
