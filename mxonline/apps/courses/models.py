# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from organization.models import CoursesOrg,Teacher
from django.db import models

# Create your models here.


class Course(models.Model):
    org = models.ForeignKey(CoursesOrg,verbose_name=u"课程机构")
    teacher = models.ForeignKey(Teacher,verbose_name="教学老师")
    name = models.CharField(max_length=50,verbose_name=u"课程名")
    desc = models.CharField(max_length=300,verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(verbose_name=u"难度",choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=5)
    learn_time = models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums =models.IntegerField(default=0,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name=U"封面")
    click_num = models.IntegerField(default=0,verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
    category = models.CharField(max_length=20, verbose_name=u"课程类别",default="后端开发")
    tag = models.CharField(max_length=10, verbose_name=u"标签",default="")
    notice =  models.CharField(max_length=100, verbose_name=u"课程公告",default="")
    teacher_tell = models.CharField(max_length=100, verbose_name=u"老师告诉你",default="")
    youneed_konw = models.CharField(max_length=100, verbose_name=u"须知",default="")
    is_banner = models.BooleanField(default=False,verbose_name=u"是否輪播")
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
    def get_lesson_nums(self):
        return len(self.lesson_set.all())

    def get_course_lesson(self):
        return self.lesson_set.all()

        return
    def get_learner(self):
        """获取课程用户
        前端代码{% for user_course in course_detail.get_learner %}
        {{ MEDIA_URL }}{{ user_course.user.image}}
        获取learner的头像
        course  与user 通过usercourse进行关联


        """
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default= datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
    def get_lesson_video(self):
        return self.video_set.all()







class Video(models.Model):
    lesson =models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100,verbose_name=u"视频")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    learn_time = models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    url = models.CharField(max_length=500,verbose_name=u"视频链接",default="")
    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class CourseResourse(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"课程资源")
    download = models.FileField(upload_to="course/resourse/%Y%m",verbose_name=u"下载",max_length=100)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name