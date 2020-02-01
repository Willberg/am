# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import DEFAULT_FILE_DIR
from user.utils import encrypt
from user.utils.result import Result


class UploadView(APIView):

    @staticmethod
    def post(request):
        ret = Result()
        suffix = str(request.FILES['file'].name).split(".")[-1]
        fn = encrypt.digest_random() + '.' + suffix

        with open(DEFAULT_FILE_DIR + fn, 'wb') as f:
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)

        ret.data = fn
        return JsonResponse(ret.serializer())
