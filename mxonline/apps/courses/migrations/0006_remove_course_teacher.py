# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-22 16:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
    ]