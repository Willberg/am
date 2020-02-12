from django.urls import path

from fs.views import RtzUploadView, TmpUploadView, RtzListView, RtzImgView

app_name = 'fs'

urlpatterns = [
    path('rtz/upload', RtzUploadView.as_view(), name='upload rtz'),
    path('rtz/list', RtzListView.as_view(), name='list rtz'),
    path('rtz/img', RtzImgView.as_view(), name='show rtz image'),

    path('tmp/upload', TmpUploadView.as_view(), name='upload tmp file'),
]
