# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/25 18:00'
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class LoginRequireMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequireMixin, self).dispatch(request,*args,**kwargs)