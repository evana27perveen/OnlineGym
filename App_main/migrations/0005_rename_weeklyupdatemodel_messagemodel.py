# Generated by Django 3.2.16 on 2023-02-01 07:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_main', '0004_weeklyupdatemodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeeklyUpdateModel',
            new_name='MessageModel',
        ),
    ]
