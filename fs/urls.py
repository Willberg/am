from django.urls import path

from fs.views import UploadView

app_name = 'fs'

urlpatterns = [
    path('upload', UploadView.as_view(), name='upload'),
]
