# user相关缓存
CACHE_USER = 'am_user'


def create_key(scope, key):
    return scope + '_' + str(key)
