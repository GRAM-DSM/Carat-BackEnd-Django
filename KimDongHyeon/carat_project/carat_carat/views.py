from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

import jwt
from django.views import View
from .models import Profiles, Users, Carings, Recarings, CaratList
from carat_project.settings import SECRET_KEY, MEDIA_ROOT, MEDIA_URL  # 토큰 발행에 사용할 secret key, 이미지를 저장할 경로 MEDIA_ROOT
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
import time


def login_decorator(func):
    """ 로그인했는지 여부를 인증하는 데코레이터 """
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            request.user = Users.objects.get(email=payload['email'])
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message': '토큰의 서명이 만료되었습니다!'}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': '존재하지 않는 토큰 값입니다!'}, status=400)
        except Users.DoesNotExist:
            return JsonResponse({'message': '토큰의 사용자 값이 존재하지 않습니다!'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper


# caring API
# https://app.gitbook.com/@carat-1/s/gogo/1./undefined-1

class create_caring(View):
    @login_decorator
    def post(self, request):
        """ 캐링 생성하기 """
        print('게시자:', request.user.email, '본문:', request.POST['caring'])
        caring = Carings(
            user_email=Users.objects.get(email=request.user.email),
            caring=request.POST['caring'],
            image='',
            carat_count=0,   # TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST
            recaring_count=0,   # TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST
            created_at=time.strftime('%Y-%m-%d %I:%M:%S', time.gmtime(timezone.now().timestamp())),
        )
        caring.save()
        return JsonResponse({'created_caring_id': caring.id}, status=200)


class edit_caring(View):
    def get(self, request, id):
        """ 캐링 가져오기 """
        pass

    @login_decorator
    def post(self, request, id):
        """ 캐링 수정하기 """
        try:
            print('수정하는사람:', request.user.email)
            if Carings.objects.filter(id=id).exists():
                profile = Profiles.objects.get(user_email=request.user.email)
                print('name:', request.POST['name'],
                      'about_me:', request.POST['about_me'],
                      '\nprofile_image:', request.FILES['profile_image'],
                      '\ncover_image:', request.FILES['cover_image'])
                profile.name = request.POST['name']
                profile.about_me = request.POST['about_me']
                profile.profile_image = request.FILES['profile_image']
                profile.cover_image = request.FILES['cover_image']
                profile.save()
                return HttpResponse(status=200)
            return JsonResponse({'message': '수정할 캐링이 존재하지 않습니다!'}, status=404)
        finally:
            pass

    @login_decorator
    def delete(self, request, id):
        """ 캐링 삭제하기 """
        try:
            if Carings.objects.filter(id=id).exist():
                target = Carings.objects.get(id=id)
                if target.user_email == Users.objects.get(email=request.user.email):
                    print('삭제할 캐링:', target.values())
                    target.delete()
                    return HttpResponse(status=200)
                return JsonResponse({'message': '삭제할 권한이 없습니다! (내가 생성한 캐링이 아님)'}, status=403)
            return JsonResponse({'message': '삭제할 캐링이 존재하지 않습니다!'}, status=404)
        except KeyError:
            return JsonResponse({"message": "해당 유저를 탈퇴할 수 없습니다!"}, status=400)


# carat API
# https://app.gitbook.com/@carat-1/s/gogo/1./undefined-2

class do_carat(View):
    @login_decorator
    def post(self, request, id):
        """ 캐럿 하기 """
        pass

    @login_decorator
    def delete(self, request, id):
        """ 캐럿 취소 """
        pass


class read_carat_list(View):
    @login_decorator
    def get(self, request):
        """ 캐럿 리스트 가져오기 """
        pass


# re-caring API
# https://app.gitbook.com/@carat-1/s/gogo/1./undefined-3

class do_recaring(View):
    @login_decorator
    def post(self, request, id):
        """ 리캐링 생성하기 """

    @login_decorator
    def delete(self, request, id):
        """ 리캐링 취소하기 """


# timeline API
# https://app.gitbook.com/@carat-1/s/gogo/1./undefined

class read_timeline(View):
    def get(self, request):
        """ 타임라인 가져오기 """
        pass


class read_profile_timeline(View):
    def get(self, request, email):
        """ 프로필 타임라인 가져오기 """
        pass
