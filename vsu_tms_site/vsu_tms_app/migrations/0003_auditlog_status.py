# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vsu_tms_app', '0002_tasklistitem_in_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='status',
            field=models.CharField(default='complete', max_length=64),
            preserve_default=False,
        ),
    ]
