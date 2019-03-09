# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/17 12:21'

import xadmin
from .models import Course,Lesson,Video,CourseResourse


class Courseadmin(object):
    list_display = ['name','desc','detail','degree','learn_time','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter = ['name','desc','detail','degree','learn_time','students']
class Lessonadmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']

class Videoadmin(object):

    list_display = ['lesson', 'name','url','add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name','url', 'add_time']
class CourseResourseadmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download','add_time']



xadmin.site.register(Course,Courseadmin)
xadmin.site.register(Lesson,Lessonadmin)
xadmin.site.register(Video,Videoadmin)
xadmin.site.register(CourseResourse,CourseResourseadmin)





