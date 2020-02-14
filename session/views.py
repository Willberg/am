import logging

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import SESSION_ID
from am.utils.cache import create_key, CACHE_USER
from am.utils.errors import CODE_WRONG_AUTHENTICATION_INFO, get_error_message
from am.utils.result import Result
from session.utils.auth import Authentication

log = logging.getLogger('django')


class SessionView(APIView):
    # 用户服务之间的相互验证
    authentication_classes = [Authentication, ]

    @staticmethod
    def post(request):
        # 只要请求将cookies传过来就可以正确找到session
        uid = request.session.get(SESSION_ID)

        result = Result()
        if not uid:
            result.code = CODE_WRONG_AUTHENTICATION_INFO
            result.message = get_error_message(result.code)
            return JsonResponse(result.serializer())

        user_dict = cache.get(create_key(CACHE_USER, uid))
        result.data = user_dict
        return JsonResponse(result.serializer())
