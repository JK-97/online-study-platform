# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/18 16:37'
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM

def random_str():
    random = Random()
    code = str(random.random())
    return code

def send_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email =email
    email_record.send_type = send_type
    email_record.save()
    email_title = ''
    email_body = ''
    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(subject=email_title,message=email_body,from_email=EMAIL_FROM,recipient_list=[email])
        return send_status

    elif send_type == "forget":
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的链接重置你的账号：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        return send_status
    elif send_type == "update_email":
        email_title = "慕学在线网邮箱修改链验证码"
        email_body = "你的邮箱验证码为{0}".format(code)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        return send_status,code


