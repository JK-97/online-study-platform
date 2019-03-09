# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/17 23:25'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':'用户名不能为空'})
    password = forms.CharField(required=True,min_length=5,error_messages={'required':"密码不能为空",'min_length':"密码长度小于5"})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空'})
    password = forms.CharField(required=True, min_length=5,error_messages={'required': "密码不能为空", 'min_length': "密码长度小于5"})
    captcha = CaptchaField(error_messages={'Invalid':"验证码错误",'required':"请输入验证码"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空'})
    captcha = CaptchaField(error_messages={'Invalid': "验证码错误", 'required': "请输入验证码"})



class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5,error_messages={'required':"密码不能为空",'min_length':"密码长度小于5"})
    password2 = forms.CharField(required=True,min_length=5,error_messages={'required':"密码不能为空",'min_length':"密码长度小于5"})


class UploadImageForm(forms.ModelForm):
    class Meta:
        model =  UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model =  UserProfile
        fields = ['nick_name','gender','birday','address','mobile']

