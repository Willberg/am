from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from am.settings import SESSION_ID
from am.utils.cache import create_key, CACHE_USER
from user.models import UserInfo
from user.serializers import UserInfoSerializer


class Authentication(BaseAuthentication):
    """用于用户登录验证"""

    def authenticate(self, request):
        uid = request.session.get(SESSION_ID)
        if not uid:
            raise exceptions.AuthenticationFailed('用户未登录')

        user_dict = cache.get(create_key(CACHE_USER, uid))
        # 缓存中不存在从数据库中取值,并更新到缓存
        if not user_dict:
            user = UserInfo.objects.filter(id=uid).first()
            if user:
                # json序列化,并存入缓存
                user_dict = UserInfoSerializer(user, many=False).data
                cache.set(create_key(CACHE_USER, uid), user_dict)

        if not user_dict:
            raise exceptions.AuthenticationFailed('用户未登录')

        user = UserInfo()
        user.__dict__ = user_dict
        # 在rest framework内部会将这两个字段赋值给request，以供后续操作使用
        return user, None

    def authenticate_header(self, request):
        pass
