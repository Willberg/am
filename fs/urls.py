from django.urls import path

from fs.views import UploadView, TestView

app_name = 'fs'

urlpatterns = [
    path('upload', UploadView.as_view(), name='upload'),
    path('test', TestView.as_view(), name='test'),
]
