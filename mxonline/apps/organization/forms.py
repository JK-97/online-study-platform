# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/21 23:06'


import re
from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
   def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        TEL_REGEXP = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        p = re.compile(TEL_REGEXP)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码违法", code="mobile_invaild")
   class Meta:
       model = UserAsk
       fields=['name','mobile','course_name']


