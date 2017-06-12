import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.join(ROOT_DIR, 'django_app')
CONF_DIR = os.path.join(ROOT_DIR, '.conf')
CONF_DOCKER_DIR = os.path.join(CONF_DIR, 'docker_conf')
CONF_DOCKER_FILE = os.path.join(CONF_DOCKER_DIR, 'settings.json')

CONF_SECRET_DIR = os.path.join(ROOT_DIR, '.conf_secret')
CONF_SECRET_COMMON_FILE = os.path.join(CONF_SECRET_DIR, 'settings_common.json')
CONF_SECRET_LOCAL_FILE = os.path.join(CONF_SECRET_DIR, 'settings_local.json')

# Secret config
if not os.path.exists(CONF_SECRET_DIR):
    os.makedirs(CONF_SECRET_DIR)
if not os.path.exists(CONF_SECRET_COMMON_FILE):
    open(CONF_SECRET_COMMON_FILE, 'wt').write('{}')
if not os.path.exists(CONF_SECRET_LOCAL_FILE):
    open(CONF_SECRET_LOCAL_FILE, 'wt').write('{}')

# Public config (Docker)
config_docker = json.loads(open(CONF_DOCKER_FILE).read())
config_secret_common = json.loads(open(CONF_SECRET_COMMON_FILE).read())
config_secret_local = json.loads(open(CONF_SECRET_LOCAL_FILE).read())
