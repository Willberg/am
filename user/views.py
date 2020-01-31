# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import UserInfo, UserToken
from .utils import encrypt
from .utils.errors import CODE_WRONG_AUTHENTICATION_INFO, get_error_message
from .utils.result import Result


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        ret = Result()



class LoginView(APIView):
    # authentication_classes里面为空，代表不需要认证
    authentication_classes = []

    def post(self, request, *args, **kwargs):
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
        UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        return JsonResponse(ret)


class LogoutView(APIView):
    pass
