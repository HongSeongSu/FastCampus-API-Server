import argparse
import json
import os
import sys

from build_util import *

ROOT_DIR = os.path.dirname(__file__)
CONF_DIR = os.path.join(ROOT_DIR, '.conf')
CONF_DOCKER_DIR = os.path.join(CONF_DIR, 'docker_conf')

CONF_SECRET_DIR = os.path.join(ROOT_DIR, '.conf_secret')
CONF_SECRET_COMMON_FILE = os.path.join(CONF_SECRET_DIR, 'settings_common.json')
CONF_SECRET_LOCAL_FILE = os.path.join(CONF_SECRET_DIR, 'settings_local.json')

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

MODE_BASE_APT = 'base_apt'
MODE_BASE_PIP = 'base_pip'
MODE_BASE_NPM = 'base_npm'
MODE_DEBUG = 'debug'
MODE_PRODUCTION = 'production'
MODE_DOCKERHUB = 'dockerhub'
parser = argparse.ArgumentParser(description='Build command', usage=USAGE)
parser.add_argument('-m', '--mode', type=str, default=MODE_PRODUCTION)
parser.add_argument('-i', '--image', type=bool, default=False)
args = parser.parse_args()

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
    msg='DockerImage Created Root Name',
    dic=config_secret_common['docker'],
    key='createdImageRootName'
)
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


docker_build = DockerBuild(CONF_DOCKER_DIR)
dockerfile = ''
dockerfile_format_dict = {
    'github_username': config_secret_common['github']['username'],
    'github_password': config_secret_common['github']['password'],
}
# print('======================')
# print('   Build Dockerfile   ')
# print('======================')
# # print('Categories : {}'.format(', '.join([category['title'] for category in categories])))
# for category in categories:
#     print('Category [{}]'.format(category['title']))
#     if len(category['options']) == 1:
#         cur_option = category['options'][0]
#         print(' Selected option: {}.{}'.format(
#             ['order'],
#             cur_option['title']
#         ))
#         dockerfile_format_dict['from_image'] = cur_option['from_image']
#         cur_string = open(os.path.join(cur_option['path'])).read().format(**dockerfile_format_dict)



sys.exit(0)

# Create Dockerfile
common_format_dict = {
    'github_username': config_secret_common['github']['username'],
    'github_password': config_secret_common['github']['password'],
}
dockerfile_template = open(os.path.join(CONF_DOCKER_DIR, '00_template.docker'), 'rt').read()
dockerfile_base_apt = open(os.path.join(CONF_DOCKER_DIR, '01_base_1_apt.docker'),
                           'rt').read().format(**common_format_dict)
dockerfile_base_pip = open(os.path.join(CONF_DOCKER_DIR, '01_base_2_pip.docker'),
                           'rt').read().format(**common_format_dict)
dockerfile_base_npm = open(os.path.join(CONF_DOCKER_DIR, '01_base_3_npm.docker'),
                           'rt').read().format(**common_format_dict)
dockerfile_common = open(os.path.join(CONF_DOCKER_DIR, '02_common.docker'), 'rt').read().format(
    **common_format_dict)
dockerfile_extra_debug = open(os.path.join(CONF_DOCKER_DIR, '03_extra_debug.docker'), 'rt').read()
dockerfile_extra_production = open(os.path.join(CONF_DOCKER_DIR, '04_extra_production.docker'),
                                   'rt').read()
format_dict = {
    'from': config_docker['imageNameRoot'],
    'maintainer': config_secret_common['docker']['maintainer'],
    'base_apt': dockerfile_base_apt,
    'base_pip': dockerfile_base_pip,
    'base_npm': dockerfile_base_npm,
    'common': dockerfile_common,
    'extra': '',
}
if args.mode == MODE_BASE_APT:
    dockerfile_name = config_docker['dockerfileBaseNameApt']
    format_dict['base_pip'] = ''
    format_dict['base_npm'] = ''
    format_dict['common'] = ''
elif args.mode == MODE_BASE_PIP:
    dockerfile_name = config_docker['dockerfileBaseNamePip']
    format_dict['from'] = config_docker['imageNameBaseApt']
    format_dict['base_apt'] = ''
    format_dict['base_npm'] = ''
    format_dict['common'] = ''
elif args.mode == MODE_BASE_NPM:
    dockerfile_name = config_docker['dockerfileBaseNameNpm']
    format_dict['from'] = config_docker['imageNameBasePip']
    format_dict['base_apt'] = ''
    format_dict['base_pip'] = ''
    format_dict['common'] = ''
elif args.mode == MODE_DEBUG:
    dockerfile_name = config_docker['dockerfileDebugName']
    format_dict['from'] = config_docker['imageNameBaseNpm']
    format_dict['base_apt'] = ''
    format_dict['base_pip'] = ''
    format_dict['base_npm'] = ''
    format_dict['extra'] = dockerfile_extra_debug
elif args.mode == MODE_PRODUCTION:
    dockerfile_name = config_docker['dockerfileProductionName']
    format_dict['from'] = config_docker['imageNameBaseNpm']
    format_dict['base_apt'] = ''
    format_dict['base_pip'] = ''
    format_dict['base_npm'] = ''
    format_dict['extra'] = dockerfile_extra_production
else:
    dockerfile_name = config_docker['dockerfileDockerHubName']
    format_dict['from'] = config_docker['imageNameDockerHub']
    format_dict['base_apt'] = ''
    format_dict['base_pip'] = ''
    format_dict['base_npm'] = ''
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
if args.mode == MODE_BASE_APT:
    build_format_dict['name'] = config_docker['imageNameBaseApt']
elif args.mode == MODE_BASE_PIP:
    build_format_dict['name'] = config_docker['imageNameBasePip']
elif args.mode == MODE_BASE_NPM:
    build_format_dict['name'] = config_docker['imageNameBaseNpm']
elif args.mode == MODE_DEBUG:
    build_format_dict['name'] = config_docker['imageNameDebug']
elif args.mode == MODE_PRODUCTION:
    build_format_dict['name'] = config_docker['imageNameDockerHub']
elif args.mode == MODE_DOCKERHUB:
    build_format_dict['name'] = config_docker['imageNameProduction']
else:
    sys.exit('Build mode is not valid')
build_command = build_command_template.format(**build_format_dict)

print('Build command execute: {}'.format(build_command))
subprocess.run(build_command, shell=True)
sys.exit('Dockerfile, DockerImage created\n  Dockerfile: {}\n  DockerImage: {}'.format(
    dockerfile_name,
    build_format_dict['name']
))
