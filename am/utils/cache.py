# user相关缓存
CACHE_USER = 'am_user'

# 文件操作相关缓存
CACHE_FS_RTZ = 'am_fs_rtz'


def create_key(scope, key):
    return scope + '_' + str(key)
