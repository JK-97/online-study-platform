# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/17 13:07'

import xadmin
from .models import CoursesOrg,Teacher,CityDict


class CityDictadmin(object):
    list_display = [ 'name', 'desc','add_time']
    search_fields = [ 'name', 'desc']
    list_filter = ['name', 'desc','add_time']

class CoursesOrgadmin(object):
    list_display = ['name', 'desc', 'city','fav_nums','click_nums']
    search_fields = ['name', 'desc', 'city','fav_nums','click_nums']
    list_filter = ['name', 'desc', 'city','fav_nums','click_nums']
class Teacheradmin(object):
    list_display = ['org', 'name', 'work_years','work_company']
    search_fields = ['org', 'name', 'work_years','work_company']
    list_filter = ['org__name', 'name', 'work_years','work_company']


xadmin.site.register(CityDict,CityDictadmin)
xadmin.site.register(CoursesOrg,CoursesOrgadmin)
xadmin.site.register(Teacher,Teacheradmin)

