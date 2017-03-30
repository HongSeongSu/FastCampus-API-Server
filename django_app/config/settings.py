"""
Django settings for FastCampus iOS API Server project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
"""
import json
import os
import sys

DEBUG = (len(sys.argv) > 1 and sys.argv[1] == 'runserver') \
        or os.environ.get('MODE') == 'DEBUG'
USE_STORAGE_S3 = DEBUG is False or os.environ.get('STORAGE') == 'S3'
DB = os.environ.get('DB')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
CONF_PATH = os.path.join(ROOT_PATH, '.conf-secret')
CONFIG_FILE_COMMON = os.path.join(CONF_PATH, 'settings_common.json')
if 'TRAVIS' in os.environ:
    CONFIG_FILE = os.path.join(CONF_PATH, 'settings_travis.json')
elif DEBUG:
    CONFIG_FILE = os.path.join(CONF_PATH, 'settings_local.json')
else:
    CONFIG_FILE = os.path.join(CONF_PATH, 'settings_deploy.json')
config_common = json.loads(open(CONFIG_FILE_COMMON).read())
config = json.loads(open(CONFIG_FILE).read())

# common과 현재 사용설정 (local또는 deploy)를 합쳐줌
for key, key_dict in config_common.items():
    if not config.get(key):
        config[key] = {}
    for inner_key, inner_key_dict in key_dict.items():
        config[key][inner_key] = inner_key_dict

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATICFILES_DIRS = [
    STATIC_DIR,
]

# AWS
if USE_STORAGE_S3:
    AWS_ACCESS_KEY_ID = config['aws']['access_key_id']
    AWS_SECRET_ACCESS_KEY = config['aws']['secret_access_key']

    AWS_STORAGE_BUCKET_NAME = config['aws']['s3_bucket_name']
    AWS_S3_SIGNATURE_VERSION = config['aws']['s3_signature_version']
    AWS_S3_HOST = 's3.{}.amazonaws.com'.format(config['aws']['s3_region'])
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

    # django-storages
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'config.storages.StaticStorage'
    STATIC_URL = 'https://{}/{}/'.format(
        AWS_S3_CUSTOM_DOMAIN,
        STATICFILES_LOCATION
    )

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
    MEDIA_URL = 'https://{}/{}/'.format(
        AWS_S3_CUSTOM_DOMAIN,
        MEDIAFILES_LOCATION
    )
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_root')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

# django-rest-auth
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'member.serializers.UserSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'member.serializers.SignupSerializer',
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    'member',
    'post',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config['db']['engine'],
        'NAME': config['db']['name'],
        'USER': config['db']['user'],
        'PASSWORD': config['db']['password'],
        'HOST': config['db']['host'],
        'PORT': config['db']['port']
    }
}
if DB == 'LOCAL':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# Auth
AUTH_USER_MODEL = 'member.MyUser'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ALLOWED_HOSTS = config['django']['allowed_hosts']
SECRET_KEY = config['django']['secret_key']
WSGI_APPLICATION = 'config.wsgi.application'
