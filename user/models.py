# Create your models here.
import time

from django.db import models


class UserInfo(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )

    LANGUAGE_CHOICES = (
        ('CN', '汉语'),
        ('EN', '英语'),
    )

    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    user_type = models.IntegerField(choices=USER_TYPE)
    language = models.CharField(max_length=4, choices=LANGUAGE_CHOICES, default='EN')
    create_time = models.BigIntegerField(default=int(round(time.time() * 1000)))
    update_time = models.BigIntegerField(default=int(round(time.time() * 1000)))


class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
