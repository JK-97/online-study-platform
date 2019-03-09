# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/23 16:20'

from .views import UserCenterView,UserFavCourseCenterView,UserFavOrgCenterView,UserFavTeacherCenterView,UserMessageCenterView,UserMyCourseView,UpLoadImageView,UpdatePwdView,SendEmailView,UpdateEmailView,UserInfoSaveView
from django.conf.urls import url,include


urlpatterns = [

    url('^info/(?P<user_id>\d+)', UserCenterView.as_view(), name="info"),

    url('^fav_course/(?P<user_id>\d+)', UserFavCourseCenterView.as_view(), name="fav_course"),

    url('^my_course/(?P<user_id>\d+)', UserMyCourseView.as_view(), name="my_course"),

    url('^fav_org/(?P<user_id>\d+)', UserFavOrgCenterView.as_view(), name="fav_org"),

    url('^fav_teacher/(?P<user_id>\d+)', UserFavTeacherCenterView.as_view(), name="fav_teacher"),

    url('^my_messages/(?P<user_id>\d+)', UserMessageCenterView.as_view(), name="my_messages"),

    #用户头像上传
    url('^image/upload/$', UpLoadImageView.as_view(), name="image_upload"),
    #用户个人中心修改密码
    url('^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    #修改邮箱 发送验证码
    url('^sendemail_code/$', SendEmailView.as_view(), name="sendemail_code"),
    url('^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    url('^info_save/$', UserInfoSaveView.as_view(), name="info_svae"),

]


#全局404界面
handler404 = 'user.view.page_not_found'
#要在seeting中將debug設置為false
handler500 = 'user.view.page_error'