from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from am.settings import SESSION_SERVICE


class Authentication(BaseAuthentication):
    """用于服务验证"""

    def authenticate(self, request):
        # headers里-会被处理掉，尽量不带-
        service_name = request.headers['service']
        secret = request.headers['secret']

        if not service_name or not secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        session_dict = SESSION_SERVICE
        if not session_dict:
            raise exceptions.AuthenticationFailed('找不到服务')

        if session_dict['secret'] != secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        return session_dict, None

    def authenticate_header(self, request):
        pass
