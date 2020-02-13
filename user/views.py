# Create your views here.
import logging

from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import SESSION_ID
from am.utils import encrypt
from am.utils.cache import CACHE_USER, create_key
from am.utils.errors import CODE_WRONG_AUTHENTICATION_INFO, get_error_message, CODE_SYS_DB_ERROR, CODE_USERNAME_EXISTED
from am.utils.result import Result
from .models import UserInfo
from .serializers import UserInfoSerializer
from .utils.permission import VIPPermission

log = logging.getLogger('django')


class RegisterView(APIView):
    authentication_classes = []

    @staticmethod
    def post(request):
        username = request._request.POST.get('username')
        password = request._request.POST.get('password')
        password = encrypt.digest(password)
        language = request._request.POST.get('language')
        if not language:
            language = 'EN'
        user = UserInfo(username=username, password=password, language=language, user_type=1)

        result = Result()
        try:
            u = UserInfo.objects.filter(username=username).first()
            if u:
                result.code = CODE_USERNAME_EXISTED
                result.message = get_error_message(result.code, language)
                return JsonResponse(result.serializer())

            with transaction.atomic():
                user.save()
                # 保存到缓存
                user_dict = UserInfoSerializer(user, many=False).data
                cache.set(create_key(CACHE_USER, user.id), user_dict, timeout=None)
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)

        # 设置session
        request.session[SESSION_ID] = user.id

        # 隐藏密码
        u = UserInfoSerializer(user, many=False).data
        u['password'] = "xxxxxx"
        result.data = u
        return JsonResponse(result.serializer())


class LoginView(APIView):
    # authentication_classes里面为空，代表不需要认证
    authentication_classes = []

    @staticmethod
    def post(request):
        result = Result()
        username = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        pwd = encrypt.digest(pwd)
        language = request._request.POST.get('language')
        if not language:
            language = 'EN'
        user = UserInfo.objects.filter(username=username, password=pwd).first()
        if not user:
            result.code = CODE_WRONG_AUTHENTICATION_INFO
            result.message = get_error_message(result.code, language)
            return JsonResponse(result.serializer())
        # 设置session
        request.session[SESSION_ID] = user.id

        # json序列化,并存入缓存
        user_dict = UserInfoSerializer(user, many=False).data
        cache.set(create_key(CACHE_USER, user.id), user_dict, timeout=None)

        # 隐藏密码
        u = UserInfoSerializer(user, many=False).data
        u['password'] = "xxxxxx"
        result.data = u
        return JsonResponse(result.serializer())


class LogoutView(APIView):
    @staticmethod
    def post(request):
        result = Result()
        request.session.flush()
        return JsonResponse(result.serializer())


class ChangePasswordView(APIView):
    permission_classes = [VIPPermission, ]

    @staticmethod
    def post(request):
        result = Result()
        old_pwd = request._request.POST.get('oldPassword')
        old_pwd = encrypt.digest(old_pwd)
        new_pwd = request._request.POST.get('newPassword')
        new_pwd = encrypt.digest(new_pwd)

        uid = request.session.get(SESSION_ID)
        user_dict = cache.get(create_key(CACHE_USER, uid))
        user = UserInfo()
        user.__dict__ = user_dict
        language = user.language
        if user.password != old_pwd:
            result.code = CODE_WRONG_AUTHENTICATION_INFO
            result.message = get_error_message(result.code, language)
            return JsonResponse(result.serializer())

        try:
            # 更新密码
            with transaction.atomic():
                UserInfo.objects.filter(id=uid).update(password=new_pwd)
                user.password = new_pwd
                # 更新缓存
                u = UserInfoSerializer(user, many=False).data
                cache.set(create_key(CACHE_USER, uid), u, timeout=None)

                # 隐藏密码
                u['password'] = "xxxxxx"
                result.data = u
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)
        return JsonResponse(result.serializer())
