# user相关缓存
CACHE_USER = 'am_user'

# 服务字典
CACHE_LOCAL_SERVICE = 'am_local_service'


def create_key(scope, key):
    return scope + '_' + str(key)
