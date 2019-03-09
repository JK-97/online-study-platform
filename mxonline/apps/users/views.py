# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import UploadImageForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, HttpResponseRedirect
import simplejson
import json
from utils.email_send import send_email
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner
from utils.mixin_utils import LoginRequireMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course, CoursesOrg, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


# Create your views here.

# 自动获取active_code
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html", {'is_active': "1"})


# 基于类的
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            try:
                user_profile.save()
            except:
                return render(request, "register.html", {'register_form': register_form, 'msg': '用户已存在'})
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "慕學在綫網歡迎你"
            user_message.save()
            send_email(user_name)
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名未激活,请到邮箱激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogOutView(View):
    """用戶登出"""

    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


# 自定义登录后代  需要再setting中配置
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 基于方法的
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        # user = User.objects.create_user("smj123456","11@qq.com","smj123456")
        # user.save()
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})
    elif request.method == "GET":
        return render(request, "login.html", {})
    # urls 中调用user_login(),返回一个view界面和原来的request对象


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_status = send_email(email, send_type="forget")
            if send_status:
                return render(request, "send_successs.html")
            else:
                return render(request, "send_fail.html")
        else:
            return render(request, "forgetpwd.html", {'forgetpwd_form': forgetpwd_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code,send_type="forget")
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {'email': email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """用户修改密码"""

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email': email, 'msg': "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "reset_pwd_success.html")
        else:
            return render(request, "password_reset.html", {'email': email, 'modify_form': modify_form})


class UserCenterView(View):
    """用户个人中心信息"""

    def get(self, request, user_id):
        # user = request.user

        user = UserProfile.objects.get(id=user_id)
        return render(request, "usercenter-info.html", {
            "user": user,
        })


class UserMyCourseView(View):
    """用户个人中心课程"""

    def get(self, request, user_id):
        # user = request.user
        own_courses = UserCourse.objects.filter(user_id=user_id)
        courses_ids = [course_user.course.id for course_user in own_courses]
        courses = Course.objects.filter(id__in=courses_ids)
        return render(request, "usercenter-mycourse.html", {
            "courses": courses,
        })


class UserFavCourseCenterView(View):
    """用户个人中心收藏课程"""

    def get(self, request, user_id):
        # user = request.user
        # user = request.user
        fav_coursess = UserFavorite.objects.filter(user_id=user_id, fav_type=1)
        courses_ids = [per_fav.fav_id for per_fav in fav_coursess]
        courses = Course.objects.filter(id__in=courses_ids)
        user = UserProfile.objects.get(id=user_id)
        return render(request, "usercenter-fav-course.html", {
            "courses": courses,
        })


class UserFavOrgCenterView(View):
    """用户个人中心收藏机构"""

    def get(self, request, user_id):
        # user = request.user
        user_fav_org = UserFavorite.objects.filter(user_id=user_id, fav_type=2)
        org_ids = [per_fav.fav_id for per_fav in user_fav_org]
        orgs = CoursesOrg.objects.filter(id__in=org_ids)

        return render(request, "usercenter-fav-org.html", {
            "orgs": orgs,
        })


class UserFavTeacherCenterView(View):
    """用户个人中心收藏讲师"""

    def get(self, request, user_id):
        # user = request.user
        user_fav_teacher = UserFavorite.objects.filter(user_id=user_id, fav_type=3)
        teacher_ids = [per_fav.fav_id for per_fav in user_fav_teacher]
        teachers = Teacher.objects.filter(id__in=teacher_ids)

        return render(request, "usercenter-fav-teacher.html", {
            "teachers": teachers,
        })


class UserMessageCenterView(LoginRequireMixin, View):
    """用户个人中心消息"""

    def get(self, request, user_id):
        # user = request.user
        user = UserProfile.objects.get(id=user_id)
        user_id = user.id
        all_messages = UserMessage.objects.filter(user=user_id)
        # 用戶進入消息頁面清空唯獨消息記錄
        all_unread_message = UserMessage.objects.filter(has_read=False, user=user_id)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(object_list=all_messages, request=request, per_page=4)

        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


class UpLoadImageView(LoginRequireMixin, View):
    """用户修改头像"""

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse(simplejson.dumps({"status": 'success'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({"status": 'fail'}), content_type='application/json')


class UpdatePwdView(View):
    """个人中心修改密码"""

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            # 判断两次密码是否一致
            pwd1 = request.POST.get('password1', '')  # 与html中name值一样
            pwd2 = request.POST.get('password2', '')  # 与html中name值一样
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type="application/json")
            # 密码加密保存
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse(simplejson.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(LoginRequireMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"exist", "msg":"邮箱已存在"}', content_type="application/json")
        _, code = send_email(email, "update_email")
        return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type="application/json")


class UpdateEmailView(LoginRequireMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        user = UserProfile.objects.get(email=request.user.email)
        code = request.POST.get('code', '')
        has_exist = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if has_exist:
            user.email = email
            user.save()
            return HttpResponse('{"status":"success", "msg":"邮箱修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"msg":"修改失败"}', content_type="application/json")

class UserInfoSaveView(View):
    def post(self, request):
        # 默认新增加一个用户，所以后面要传一个实例
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(simplejson.dumps({"status": 'success'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps(user_info_form.errors), content_type='application/json')


class IndexView(View):
    def get(self, request):
        # 取出輪播圖
        all_banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:5]
        banner_course = Course.objects.filter(is_banner=True)[:15]
        course_orgs = CoursesOrg.objects.all()[:15]

        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_course": banner_course,
            "course_orgs": course_orgs,
        })


def page_not_found(request):
    # 全局404處理函數
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    # 全局500處理函數
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response
