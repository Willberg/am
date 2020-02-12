# Create your views here.
import json
import logging

from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from am.settings import DEFAULT_FILE_DIR, SESSION_ID
from am.utils import encrypt
from am.utils.cache import create_key, CACHE_FS_RTZ, CACHE_USER
from am.utils.errors import CODE_SYS_DB_ERROR, get_error_message
from am.utils.result import Result
from fs.models import TextModel, RtzDoc, Rtz
from user.utils.permission import SVIPPermission

log = logging.getLogger('django')


class TmpUploadView(APIView):

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

    @staticmethod
    def get(req):
        result = Result()
        text = TextModel.objects()
        name = req.GET['name']
        content = req.GET['content']
        # 插入新数据
        text.create(name=name, content=content)
        return JsonResponse(result.serializer())


class RtzUploadView(APIView):
    permission_classes = [SVIPPermission, ]

    @staticmethod
    def post(request):
        result = Result()
        uid = request.session.get(SESSION_ID)
        user = cache.get(create_key(CACHE_USER, uid))
        language = user.language

        # 图片处理
        rtz_doc = RtzDoc()
        rtz_doc.photo.new_file(content_type=request.FILES['file'].content_type)
        for chunk in request.FILES['file'].chunks():
            rtz_doc.photo.write(chunk)
        rtz_doc.photo.close()

        # 保存到mongo
        try:
            rd = rtz_doc.save()
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)
            return JsonResponse(result.serializer())

        # 保存记录到数据库和缓存
        rtz = Rtz()
        rtz.doc_id = str(rd.id)
        rtz.family = request._request.POST.get('family')
        rtz.person_name = request._request.POST.get('person_name')
        rtz.tags = request._request.POST.get('tags')

        try:
            # 事务处理
            with transaction.atomic():
                rtz.save()
                cache(create_key(CACHE_FS_RTZ, rtz.id), json.dumps(rtz))
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)

        result.data = rtz
        return JsonResponse(result.serializer())


class RtzListView(APIView):
    permission_classes = [SVIPPermission, ]

    @staticmethod
    def get(request):
        result = Result()

        # 限制数量
        offset = request._request.GET.get('offset')
        count = request._request.GET.get('count')

        # 从数据库中取出list
        rtz_list = Rtz.objects.raw('select * from fs_rtz order by marks limit %s,%s' % (offset, count)).all()
        for rtz in rtz_list:
            # 从mongo中取出图片
            photo = RtzDoc.objects().get(id=rtz.doc_id).read()
            rtz.photo = photo

        result.data = rtz_list
        return JsonResponse(result.serializer())


class RtzImgView(APIView):
    permission_classes = [SVIPPermission, ]

    @staticmethod
    def get(request):
        rtz_id = request._request.GET.get('rtz_id')

        # 从缓存中取出rtz
        rtz = cache.get(create_key(CACHE_FS_RTZ, rtz_id))

        # 从mongo中取出图片
        rtz_doc = RtzDoc.objects().get(id=rtz_id)

        result = Result()
        rtz.photo = rtz_doc.photo.read()
        result.data = rtz
        return JsonResponse(result.serializer())
