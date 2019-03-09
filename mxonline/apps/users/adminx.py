# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/16 23:04'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner


#和view绑定,主题设定
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "鸡哥后台管理系统"
    site_footer = "鸡哥学习网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):

    list_display = ['code','email','send_type','send_time']
    #显示字段
    search_fields = ['code','email','send_type']
    #查找字段
    list_filter = ['code','email','send_type','send_time']
    #过滤器

class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']



xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)