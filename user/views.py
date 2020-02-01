# Create your views here.
import logging

from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import SESSION_ID
from .models import UserInfo
from .utils import encrypt
from .utils.errors import CODE_WRONG_AUTHENTICATION_INFO, get_error_message, CODE_SYS_DB_ERROR
from .utils.result import Result

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

        ret = Result()
        try:
            with transaction.atomic():
                user.save()
                # 保存到缓存
                cache.set(user.id, user)
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)

        # 设置session
        request.session[SESSION_ID] = user.id
        return JsonResponse(ret.serializer())


class LoginView(APIView):
    # authentication_classes里面为空，代表不需要认证
    authentication_classes = []

    @staticmethod
    def post(request):
        ret = Result()
        username = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        pwd = encrypt.digest(pwd)
        language = request._request.POST.get('language')
        if not language:
            language = 'EN'
        user = UserInfo.objects.filter(username=username, password=pwd).first()
        if not user:
            ret.code = CODE_WRONG_AUTHENTICATION_INFO
            ret.message = get_error_message(CODE_WRONG_AUTHENTICATION_INFO, language)
            return JsonResponse(ret.serializer())
        # 设置session
        request.session[SESSION_ID] = user.id
        return JsonResponse(ret.serializer())


class LogoutView(APIView):
    @staticmethod
    def post(request):
        ret = Result()
        request.session.flush()
        return JsonResponse(ret.serializer())


class ChangePasswordView(APIView):
    @staticmethod
    def post(request):
        ret = Result()
        old_pwd = request._request.POST.get('oldPassword')
        old_pwd = encrypt.digest(old_pwd)
        new_pwd = request._request.POST.get('newPassword')
        new_pwd = encrypt.digest(new_pwd)

        uid = request.session.get(SESSION_ID)
        user = cache.get(uid)
        language = user.language
        if user.password != old_pwd:
            ret.code = CODE_WRONG_AUTHENTICATION_INFO
            ret.message = get_error_message(ret.code, language)
            return JsonResponse(ret.serializer())

        try:
            # 更新密码
            with transaction.atomic():
                UserInfo.objects.filter(username=user.username).update(password=new_pwd)
                user.password = new_pwd
                cache.set(uid, user)
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)
        return JsonResponse(ret.serializer())
