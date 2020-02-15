from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from am.settings import LOCAL_SERVICE


class Authentication(BaseAuthentication):
    """用于服务验证"""

    def authenticate(self, request):
        # headers里-会被处理掉，尽量不带-
        service_name = request.headers['service']
        secret = request.headers['secret']

        if not service_name or not secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        if not LOCAL_SERVICE:
            raise exceptions.AuthenticationFailed('找不到服务')

        if service_name != LOCAL_SERVICE['service_name'] or secret != LOCAL_SERVICE['secret']:
            raise exceptions.AuthenticationFailed('找不到服务')

        return LOCAL_SERVICE, None

    def authenticate_header(self, request):
        pass
