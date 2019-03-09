# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import CoursesOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
import simplejson
from django.db.models import Q
# Create your views here.


class OrgListView(View):
    def get(self,request):
        all_city = CityDict.objects.all()
        all_orgs = CoursesOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        org_nums = all_orgs.count()
        city_id = request.GET.get('city', "")
        search_key = request.GET.get('keywords', '')
        if search_key:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_key) | Q(desc__icontains=search_key) )


        #城市筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        category = request.GET.get('ct','')
        #类型筛选
        if category:
            all_orgs = all_orgs.filter(category=category)
        #排序功能
        sort = request.GET.get('sort','')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            if sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        #添加分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(object_list=all_orgs, request=request,per_page=3)

        orgs = p.page(page)

        return render(request,"org-list.html",{
            'all_city':all_city,
            'all_orgs':orgs,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })

class AddUserAskView(View):
    # 处理表单提交当然post
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        # 判断该form是否有效
        vaild =userask_form.is_valid()
        if vaild:
            # 这里是modelform和form的区别
            # 它有model的属性
            # 当commit为true进行真正保存
            user_ask = userask_form.save(commit=True)
            # 这样就不需要把一个一个字段取出来然后存到model的对象中之后save

            # 如果保存成功,返回json字符串,后面content type是告诉浏览器的,
            return HttpResponse(simplejson.dumps({"status": 'success'}), content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse(simplejson.dumps({"status": 'fail',"msg":'添加出错'}),content_type='application/json')
        #原版教程      HttpResponse("{'status': 'fail','msg':'添加出错'}",content_type='application/json') 返回的不是对向

class OrgHomeView(View):

    """机构首页"""
    def get(self,request,org_id):

        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        course_org.click_nums +=1
        course_org.save()
        if  request.user.is_authenticated():
        # 判断用户登录状态
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2)
            if exist_records:
                has_fav =True
            else:
                has_fav = False
        else:
            pass
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teachers,
            'course_org':course_org,
            'current_page':'home',
            'has_fav':has_fav

        })

class OrgCourseView(View):

    """机构课程"""
    def get(self,request,org_id):

        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': 'orgcourse'
        })

class OrgDescView(View):

    """机构详情"""
    def get(self,request,org_id):

        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_desc = course_org.desc
        return render(request,'org-detail-desc.html',{
            'all_desc':all_desc,
            'course_org':course_org,
            'current_page': 'orgdesc'
        })

class OrgTeacherView(View):

    """机构教师"""
    def get(self,request,org_id):

        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()

        return render(request,'org-detail-teachers.html',{
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page': 'orgteacher'
        })

class AddFavView(View):
    """用户收藏"""
    def post(self,request):
        fav_id = request.POST.get('fav_id','0')
        fav_type = request.POST.get('fav_type','0')
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse(simplejson.dumps({"status": 'fail',"msg":'用户未登录'}),content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            if int(fav_type)== 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums-=1
                if course.fav_nums <0:
                    course.fav_nums=0
                course.save()
            elif int(fav_type)== 2:
                course_org =CoursesOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -=1
                if course_org.fav_nums <0:
                    course_org.fav_nums=0
                    course_org.save()
            elif int(fav_type)== 3:
                teacher =Teacher.objects.get(id = int(fav_id))
                teacher.fav_nums -=1
                if teacher.fav_nums <0:
                    teacher.fav_nums=0
                teacher.save()
            return HttpResponse(simplejson.dumps({"status": 'success', "msg": '收藏'}),content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:

                user_fav.user =request.user
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id=int(fav_id)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CoursesOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse(simplejson.dumps({"status": 'success', "msg": '已收藏'}),content_type='application/json')

            else:
                return HttpResponse(simplejson.dumps({"status": 'fail', "msg": '收藏出错'}), content_type='application/json')


class TeacherListView(View):
    def get(self,request):

        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        hot_teacher = all_teachers.order_by("-click")[:3]
        sort = request.GET.get('sort', '')
        search_key = request.GET.get('keywords', '')
        if search_key:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_key) | Q(desc__icontains=search_key) )
        if sort == "rq":
            all_teachers = all_teachers.order_by("-fav_nums")
        # 添加分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(object_list=all_teachers, request=request, per_page=2)

        all_teachers = p.page(page)

        return render(request,"teachers-list.html",{
            "all_teachers":all_teachers,
            "teacher_nums":teacher_nums,
            "hot_teacher" :hot_teacher,
            "sort":sort

        })



class TeacherDetailView(View):
    def get(self,request,teacher_id):

        teacher = Teacher.objects.get(id = teacher_id)
        teacher.click +=1
        teacher.fav_nums = UserFavorite.objects.filter(fav_id=teacher.id,fav_type=3).count()
        teacher.save()
        org = CoursesOrg.objects.get(teacher=teacher)
        all_teachers = Teacher.objects.all()
        hot_teacher = all_teachers.order_by("-click")[:3]
        if  request.user.is_authenticated():
        # 判断用户登录状态
            exist_records1 = UserFavorite.objects.filter(user=request.user,fav_id=teacher.id, fav_type=3)

            if exist_records1:
                has_fav1 =True

            else:
                has_fav1 = False

            exist_records2 = UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if exist_records2:
                has_fav2 = True
            else:
                has_fav2 = False
        else:
             pass
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'hot_teacher':hot_teacher,
            'org':org,
            'has_fav1':has_fav1,
            'has_fav2':has_fav2,

        })






