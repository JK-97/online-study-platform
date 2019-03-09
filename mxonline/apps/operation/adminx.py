# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/17 13:15'


import xadmin
from .models import UserAsk,UserMessage,UserCourse,UserFavorite,Course_comment


class UserAskadmin(object):
    list_display = ['name', 'mobile', 'course_name']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name']
class UserMessageadmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
class UserCourseadmin(object):
    list_display = ['user', 'course','add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__nick_name', 'course__name','add_time']
class UserFavoriteadmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']
class Course_commentadmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user__nick_name', 'course__name', 'comments', 'add_time']


xadmin.site.register(UserAsk,UserAskadmin)
xadmin.site.register(UserMessage,UserMessageadmin)
xadmin.site.register(UserCourse,UserCourseadmin)
xadmin.site.register(UserFavorite,UserFavoriteadmin)
xadmin.site.register(Course_comment,Course_commentadmin)