# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/21 23:11'

from .views import OrgListView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView
from django.conf.urls import url,include


urlpatterns = [
    url('^list/$',OrgListView.as_view(),name="list"),
    url('^add_ask/$',AddUserAskView.as_view(),name="add_ask"),
    url('^home/(?P<org_id>\d+)',OrgHomeView.as_view(),name="org_home"),
    url('^course/(?P<org_id>\d+)',OrgCourseView.as_view(),name="org_course"),
    url('^desc/(?P<org_id>\d+)',OrgDescView.as_view(),name="org_desc"),
    url('^teacher/(?P<org_id>\d+)',OrgTeacherView.as_view(),name="org_teacher"),
    #机构收藏
    url('^add_fav/$', AddFavView.as_view(), name="add_fav"),

    url('^teacher_list/$',TeacherListView .as_view(), name="teacher_list"),
    url('^teacher_detail/(?P<teacher_id>\d+)',TeacherDetailView .as_view(), name="teacher_detail"),

]