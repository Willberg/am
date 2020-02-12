from django.db import models
from mongoengine import Document, FileField, StringField


# Create your models here.
class TextModel(Document):
    name = StringField(max_length=30)
    content = StringField(max_length=255)


class RtzDoc(Document):
    photo = FileField()


# 图片model
class Rtz(models.Model):
    doc_id = models.CharField(max_length=64, unique=True)
    family = models.CharField(max_length=64)
    person_name = models.CharField(max_length=64)
    tags = models.CharField(max_length=256)
    views = models.IntegerField(default='0')
    comments = models.IntegerField(default='0')
    marks = models.IntegerField(default='0')


# 评论model
class RtzComment(models.Model):
    user_id = models.BigIntegerField()
    rtz_id = models.BigIntegerField()
    comment = models.CharField(max_length=512)
    like = models.IntegerField(default='0')
    dislike = models.IntegerField(default='0')
