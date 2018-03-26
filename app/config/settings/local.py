from .base import *

secrets = json.loads(open(SECRETS_LOCAL, 'rt').read())
set_config(secrets, module_name=__name__)

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    'server.lhy.kr',
    'api.lhy.kr',
]
WSGI_APPLICATION = 'config.wsgi.local.application'
INSTALLED_APPS += [
]

# Static
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
