# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-26 16:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_auto_20190225_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='detial',
            new_name='detail',
        ),
    ]
