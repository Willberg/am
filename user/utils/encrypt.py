# 创建唯一码
import hashlib
import time
import uuid

from am.settings import SECRET_KEY


def digest():
    k = str(round(time.time() * 1000)) + str(uuid.uuid1()).split('-')[0]
    m = hashlib.md5(k.encode('utf-8'))
    return m.hexdigest()


# 生成加密数字
def digest(o):
    # 当前时间，相当于生成一个随机的字符串
    m = hashlib.md5(bytes(o + SECRET_KEY, encoding='utf-8'))
    return m.hexdigest()