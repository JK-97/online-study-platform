# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/23 16:20'

from .views import CourseView,CourseDetailView,CourseVideoView,CourseCommentView,AddCommentView,VideoPlayView
from django.conf.urls import url,include


urlpatterns = [
    url('^list/$',CourseView.as_view(),name="list"),
    url('^detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name="detail"),
    url('^video/(?P<course_id>\d+)', CourseVideoView.as_view(), name="video"),
    url('^comment/(?P<course_id>\d+)', CourseCommentView.as_view(), name="comment"),
    #添加课程评论  参数已经放入 post 里了所以不用加参数了
    url('^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    url('^play_video/(?P<video_id>\d+)', VideoPlayView.as_view(), name="play_video"),
]
