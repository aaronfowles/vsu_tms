# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsu_tms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklistitem',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
