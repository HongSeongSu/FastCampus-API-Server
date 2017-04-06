import argparse
import json
import os
import subprocess
import sys

ROOT_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(ROOT_DIR, '.conf')
CONF_DOCKER_DIR = os.path.join(CONF_DIR, 'docker')
CONF_FILE = os.path.join(CONF_DOCKER_DIR, 'settings.json')

CONF_SECRET_DIR = os.path.join(ROOT_DIR, '.conf-secret')
CONF_SECRET_COMMON_FILE = os.path.join(CONF_SECRET_DIR, 'settings_common.json')
CONF_SECRET_LOCAL_FILE = os.path.join(CONF_SECRET_DIR, 'settings_local.json')


# Utility functions
def dict_key_make(dic, key):
    if not dic.get(key):
        dic[key] = {}


def input_dict_value(msg, dic, key, default=None):
    while not dic.get(key) or (isinstance(dic[key], str) and dic[key].strip() == ''):
        value = input('{}: '.format(msg))
        dic[key] = value
        if default and value == '':
            dic[key] = default


# argparse
USAGE = '''Docker build commands
    -m, --mode
        [default]: Build production image from ubuntu:16.04
        base: Build base image
        debug: Build debug image from base

    -f, --file
        [default]: Make Dockerfile and Image
        True: Only make Dockerfile
'''
MODE_BASE = 'base'
MODE_DEBUG = 'debug'
MODE_PRODUCTION = 'production'
MODE_DOCKERHUB = 'dockerhub'
parser = argparse.ArgumentParser(description='Build command', usage=USAGE)
parser.add_argument('-m', '--mode', type=str, default=MODE_PRODUCTION)
parser.add_argument('-i', '--image', type=bool, default=False)
args = parser.parse_args()

# Public config
config = json.loads(open(CONF_FILE).read())

# Secret config
if not os.path.exists(CONF_SECRET_DIR):
    os.makedirs(CONF_SECRET_DIR)
if not os.path.exists(CONF_SECRET_COMMON_FILE):
    open(CONF_SECRET_COMMON_FILE, 'wt').write('{}')
if not os.path.exists(CONF_SECRET_LOCAL_FILE):
    open(CONF_SECRET_LOCAL_FILE, 'wt').write('{}')
config_secret_common = json.loads(open(CONF_SECRET_COMMON_FILE).read())
config_secret_local = json.loads(open(CONF_SECRET_LOCAL_FILE).read())

# Secret config - docker
dict_key_make(config_secret_common, 'docker')
input_dict_value(
    msg='DockerImage Maintainer Email',
    dic=config_secret_common['docker'],
    key='maintainer'
)

# Secret config - GitHub
dict_key_make(config_secret_common, 'github')
input_dict_value(
    msg='GitHub username',
    dic=config_secret_common['github'],
    key='username'
)
input_dict_value(
    msg='GitHub password',
    dic=config_secret_common['github'],
    key='password'
)

# Secret config - django
dict_key_make(config_secret_common, 'django')
dict_key_make(config_secret_common['django'], 'default_superuser')
input_dict_value(
    msg='Django default superuser username',
    dic=config_secret_common['django']['default_superuser'],
    key='username'
)
input_dict_value(
    msg='Django default superuser password',
    dic=config_secret_common['django']['default_superuser'],
    key='password'
)
input_dict_value(
    msg='Django default superuser email',
    dic=config_secret_common['django']['default_superuser'],
    key='email',
    default='',
)
dict_key_make(config_secret_local, 'django')
input_dict_value(
    msg='Django allowed hosts (default: ["*"])',
    dic=config_secret_local['django'],
    key='allowed_hosts',
    default=['*', ],
)

# Secret config - db
dict_key_make(config_secret_local, 'db')
input_dict_value(
    msg='DB Engine (default: django.db.backends.postgresql_psycopg2)',
    dic=config_secret_local['db'],
    key='engine',
    default='django.db.backends.postgresql_psycopg2',
)
input_dict_value(
    msg='DB Name (default: api-ios)',
    dic=config_secret_local['db'],
    key='name',
    default='api-ios',
)
input_dict_value(
    msg='DB Host (default: localhost)',
    dic=config_secret_local['db'],
    key='host',
    default='localhost'
)
input_dict_value(
    msg='DB Port (default: 5432)',
    dic=config_secret_local['db'],
    key='port',
    default='5432'
)
input_dict_value(
    msg='DB User',
    dic=config_secret_local['db'],
    key='user',
)
input_dict_value(
    msg='DB Password',
    dic=config_secret_local['db'],
    key='password',
)

with open(CONF_SECRET_COMMON_FILE, 'wt') as f:
    f.write(json.dumps(config_secret_common, indent=4, sort_keys=True))
with open(CONF_SECRET_LOCAL_FILE, 'wt') as f:
    f.write(json.dumps(config_secret_local, indent=4, sort_keys=True))

# Create Dockerfile
common_format_dict = {
    'github_username': config_secret_common['github']['username'],
    'github_password': config_secret_common['github']['password'],
}
dockerfile_template = open(os.path.join(CONF_DOCKER_DIR, '00_template.docker'), 'rt').read()
dockerfile_base = open(os.path.join(CONF_DOCKER_DIR, '01_base.docker'), 'rt').read().format(
    **common_format_dict)
dockerfile_common = open(os.path.join(CONF_DOCKER_DIR, '02_common.docker'), 'rt').read().format(
    **common_format_dict)
dockerfile_extra_debug = open(os.path.join(CONF_DOCKER_DIR, '03_extra_debug.docker'), 'rt').read()
dockerfile_extra_production = open(os.path.join(CONF_DOCKER_DIR, '04_extra_production.docker'),
                                   'rt').read()
format_dict = {
    'from': config['rootImageName'],
    'maintainer': config_secret_common['docker']['maintainer'],
    'base': dockerfile_base,
    'common': dockerfile_common,
    'extra': '',
}
if args.mode == MODE_BASE:
    dockerfile_name = config['dockerfileBaseName']
    format_dict['common'] = ''
elif args.mode == MODE_DEBUG:
    dockerfile_name = config['dockerfileDebugName']
    format_dict['from'] = config['baseImageName']
    format_dict['base'] = ''
    format_dict['extra'] = dockerfile_extra_debug
elif args.mode == MODE_PRODUCTION:
    dockerfile_name = config['dockerfileProductionName']
    format_dict['from'] = config['baseImageName']
    format_dict['base'] = ''
    format_dict['extra'] = dockerfile_extra_production
else:
    dockerfile_name = config['dockerfileDockerHubName']
    format_dict['from'] = config['dockerHubImageName']
    format_dict['base'] = ''
    format_dict['common'] = ''
    format_dict['extra'] = dockerfile_extra_production
dockerfile = dockerfile_template.format(**format_dict)
while True:
    do_continue = input(
        '{}\n\nDockerfile(Filename: {}) will be created as above. Do you proceed like this? [Y/n]: '.format(
            dockerfile,
            dockerfile_name))
    if do_continue == '' or do_continue.lower() == 'y':
        break
    elif do_continue.lower() == 'n':
        sys.exit('Build aborted')

with open(os.path.join(ROOT_DIR, dockerfile_name), 'wt') as f:
    f.write(dockerfile)

if args.image:
    sys.exit('Dockerfile created')

# Execute docker build command
build_command_template = 'docker build . -t {name} -f {dockerfile_name}'
build_format_dict = {
    'dockerfile_name': dockerfile_name,
}
if args.mode == MODE_BASE:
    build_format_dict['name'] = config['baseImageName']
elif args.mode == MODE_DEBUG:
    build_format_dict['name'] = config['debugImageName']
elif args.mode == MODE_PRODUCTION:
    build_format_dict['name'] = config['dockerHubImageName']
else:
    sys.exit('DockerHub mode does not build image')
build_command = build_command_template.format(**build_format_dict)

print('Build command execute: {}'.format(build_command))
subprocess.run(build_command, shell=True)
sys.exit('Dockerfile, DockerImage created')
