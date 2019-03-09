# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course,CourseResourse,Video
from organization.models import CoursesOrg
from operation.models import UserFavorite,Course_comment,UserCourse
from django.http import HttpResponse
import simplejson
from django.db.models import Q
from utils.mixin_utils import LoginRequireMixin
# Create your views here.



class CourseView(View):
    def get(self,request):
        all_course = Course.objects.all()
        sort = request.GET.get('sort', '')
        recommand_course = all_course.order_by("-click_num")[:2]
        search_key = request.GET.get('keywords', '')
        if search_key:
            all_course = all_course.filter(Q(name__icontains=search_key)|Q(desc__icontains=search_key)|Q(detail__icontains=search_key))
        if sort:
            if sort == "hot":
                all_course = all_course.order_by("-fav_nums")
            if sort == "students":
                all_course = all_course.order_by("-students")
            if sort == "new":
                all_course = all_course.order_by("-id")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(object_list=all_course, request=request, per_page=3)

        course = p.page(page)

        return render(request,"course-list.html",{
            'all_course':course,
            'sort':sort,
            'recommand_course':recommand_course,
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course_detail = Course.objects.get(id=int(course_id))
        course_detail_org = CoursesOrg.objects.get(id=int(course_detail.org_id))
        course_detail.click_num +=1
        course_detail.save()
        if request.user.is_authenticated():
        # 判断用户登录状态
            exist_course_records = UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1)
            exist_org_records = UserFavorite.objects.filter(user=request.user, fav_id=course_detail.org_id, fav_type=2)
            if exist_course_records:
                has_fav_course =True
            else:
                has_fav_course = False
            if exist_org_records:
                has_fav_org =True
            else:
                has_fav_org = False
        else:
            pass

        tag = course_detail.tag
        if tag:
            relate_course = Course.objects.filter(tag=str(tag))[:2]
        else:
            relate_course = []

        return render(request,"course-detail.html",{
            "course_detail":course_detail,
            "relate_course":relate_course,
            "course_detail_org":course_detail_org,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
        })


class CourseVideoView(LoginRequireMixin, View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))


        user_courses= UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            course.students += 1
            user_course = UserCourse(user=request.user,course=course)
            course.save()
            user_course.save()
#关联course和user


        user_courses =UserCourse.objects.filter(course=course)
        user_ids = [ user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in= user_ids)
        #取出所有课程
        course_ids = [ user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in = course_ids).order_by("-click_num")[:5]

        all_resourse = CourseResourse.objects.filter(course_id=course_id)
        return render(request,"course-video.html",{
            "course":course,
            "current_page": "video",
            "all_resourse": all_resourse,
            'relate_courses':relate_courses,
        })



class CourseCommentView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = course.course_comment_set.all()
        all_resourse = CourseResourse.objects.filter(course_id=course_id)
        return render(request, "course-comment.html", {
            "all_comments": all_comments,
            "course":course,
            "current_page":"comment",
            "all_resourse": all_resourse,
        })

class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            #用户未登录
            return HttpResponse(simplejson.dumps({"status": 'fail',"msg":'用户未登录'}),content_type='application/json')
        course_id =request.POST.get("course_id",0)
        comments = request.POST.get("comments","")
        if course_id>0 and comments:
            course_comment= Course_comment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user =request.user
            course_comment.save()
            return HttpResponse(simplejson.dumps({"status": 'success',"msg":'添加成功'}),content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({"status": 'fail',"msg":'添加失败'}),content_type='application/json')

class VideoPlayView(View):
    #视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.click_num += 1
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 关联course和user

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        all_resourse = CourseResourse.objects.filter(course_id=course.id)
        return render(request, "course_play.html", {
            "course": course,
            "current_page": "video",
            "all_resourse": all_resourse,
            'relate_courses': relate_courses,
            'video':video,
        })








