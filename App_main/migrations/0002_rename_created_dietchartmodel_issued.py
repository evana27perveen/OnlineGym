# Generated by Django 3.2.16 on 2023-01-25 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dietchartmodel',
            old_name='created',
            new_name='issued',
        ),
    ]
