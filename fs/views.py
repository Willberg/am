# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import DEFAULT_FILE_DIR
from fs.models import TextModel
from user.utils import encrypt
from user.utils.result import Result


class UploadView(APIView):

    @staticmethod
    def post(request):
        result = Result()
        suffix = str(request.FILES['file'].name).split(".")[-1]
        fn = encrypt.digest_random() + '.' + suffix

        with open(DEFAULT_FILE_DIR + fn, 'wb') as f:
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)

        result.data = fn
        return JsonResponse(result.serializer())


class TestView(APIView):
    authentication_classes = []

    @staticmethod
    def get(req):
        result = Result()
        text = TextModel.objects()
        name = req.GET['name']
        content = req.GET['content']
        # 插入新数据
        text.create(name=name, content=content)
        return JsonResponse(result.serializer())
