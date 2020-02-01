"""
Django settings for am project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ec%fyp0!@l7t)%dx@t+lmcp%$r*8uwjmh65_l^&0wgq&a*7!xh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'fs',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'am.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'am.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'},
        'NAME': 'am',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.0.103',
        'PORT': '3306',
    }
}

# 设置全局认证
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ['user.utils.auth.Authentication', ],  # 里面写你的认证的类的路径
}

# 文件存储路径
DEFAULT_FILE_DIR = "/home/john/tmp/"  # 临时文件存放路径
if not os.path.exists(DEFAULT_FILE_DIR):
    os.mkdir(DEFAULT_FILE_DIR)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# logs
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'sender@gmail.com'  # 发件箱
# EMAIL_HOST_PASSWORD = 'xxxxx'  # 开启POP3/SMTP服务
# SERVER_EMAIL = 'sender@gmail.com'  # 与发件箱一致
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# ADMINS = [('John', 'John@gmail.com'), ('Peter', 'Peter@gmail.com')]

# LOGGING_DIR 日志文件存放目录
LOGGING_DIR = "logs"  # 日志存放路径
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # 格式化器
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s][%(funcName)s][%(lineno)d] > %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s]> %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/info.log' % LOGGING_DIR,  # 具体日志文件的名字
            'formatter': 'standard'
        },  # 用于文件输出
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'formatter': 'standard'
        # },
    },
    'loggers': {  # 日志分配到哪个handlers中
        'mydjango': {
            'handlers': ['console', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        # 如果要将get,post请求同样写入到日志文件中，则这个触发器的名字必须交django,然后写到handler中
        'django': {
            'handlers': ['console', 'file_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
