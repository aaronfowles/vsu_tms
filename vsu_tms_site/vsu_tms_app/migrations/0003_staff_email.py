# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsu_tms_app', '0002_auto_20160317_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='email',
            field=models.EmailField(default=None, max_length=64),
            preserve_default=False,
        ),
    ]
