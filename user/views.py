# Create your views here.
import logging

from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import UserInfo, UserToken
from .utils import encrypt
from .utils.errors import CODE_WRONG_AUTHENTICATION_INFO, get_error_message, CODE_SYS_DB_ERROR
from .utils.result import Result

log = logging.getLogger('django')


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request._request.POST.get('username')
        password = request._request.POST.get('password')
        password = encrypt.digest(password)
        language = request._request.POST.get('language')
        if not language:
            language = 'EN'
        user = UserInfo(username=username, password=password, language=language, user_type=1)

        ret = Result()
        token = ret.token
        try:
            with transaction.atomic():
                user.save()
                UserToken.objects.update_or_create(user=user, defaults={'token': token})
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)
        return JsonResponse(ret.serializer())


class LoginView(APIView):
    # authentication_classes里面为空，代表不需要认证
    authentication_classes = []

    def post(self, request):
        ret = Result()
        username = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        pwd = encrypt.digest(pwd)
        language = request._request.POST.get('language')
        if not language:
            language = 'EN'
        obj = UserInfo.objects.filter(username=username, password=pwd).first()
        if not obj:
            ret.code = CODE_WRONG_AUTHENTICATION_INFO
            ret.message = get_error_message(CODE_WRONG_AUTHENTICATION_INFO, language)
            return JsonResponse(ret)
        # 为用户创建token
        # 存在就更新，不存在就创建
        token = ret.token
        try:
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)
        return JsonResponse(ret.serializer())


class LogoutView(APIView):
    def post(self, request):
        ret = Result()
        ret.token = None
        token = request._request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        language = user_token.user.language
        try:
            user_token.delete()
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)
        return JsonResponse(ret.serializer())


class ChangePasswordView(APIView):
    def post(self, request):
        ret = Result()
        old_pwd = request._request.POST.get('oldPassword')
        old_pwd = encrypt.digest(old_pwd)
        new_pwd = request._request.POST.get('newPassword')
        new_pwd = encrypt.digest(new_pwd)

        token = request._request.GET.get('token')
        user = UserToken.objects.filter(token=token).first().user
        language = user.language
        if user.password != old_pwd:
            ret.code = CODE_WRONG_AUTHENTICATION_INFO
            ret.message = get_error_message(ret.code, language)
            return ret

        try:
            # 更新密码
            UserInfo.objects.filter(username=user.username).update(password=new_pwd)
        except Exception as e:
            log.error(e)
            ret.code = CODE_SYS_DB_ERROR
            ret.message = get_error_message(CODE_SYS_DB_ERROR, language)
        return JsonResponse(ret.serializer())
