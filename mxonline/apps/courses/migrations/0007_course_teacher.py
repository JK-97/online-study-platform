# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-22 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20190222_2229'),
        ('courses', '0006_remove_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='\u6559\u5b66\u8001\u5e08'),
        ),
    ]
