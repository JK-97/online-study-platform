# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name=u"城市")
    desc = models.CharField(max_length=100,verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class CoursesOrg(models.Model):
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    category = models.CharField(verbose_name=u"机构类型",max_length=10,default="pxjg",choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")))
    name = models.CharField(max_length=50,verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%Y/%m",verbose_name="logo",default=None)
    adress = models.CharField(max_length=150,verbose_name=u"机构地址")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0,verbose_name=u"课程数")
    tag  = models.CharField(max_length=20,verbose_name=u"標簽",default="")



    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return  self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

class Teacher(models.Model):
    org = models.ForeignKey(CoursesOrg,verbose_name=u"所在机构")
    name = models.CharField(max_length=50,verbose_name=u"教师名称")
    work_years = models.IntegerField(default=0,verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50,verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司位置")
    points = models.CharField(max_length=50, verbose_name=u"公司职位")
    click = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(upload_to="teacher/%Y/%m",verbose_name="logo",default=None)

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name
    def get_teacher_nums(self):
        return Teacher.objects.all().count()
