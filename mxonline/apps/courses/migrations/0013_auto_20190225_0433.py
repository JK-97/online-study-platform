# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-25 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresourse',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u8bfe\u7a0b\u8d44\u6e90'),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u89c6\u9891'),
        ),
    ]