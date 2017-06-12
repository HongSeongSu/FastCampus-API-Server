import subprocess
from _utils import *


class SettingsBuild:
    def __init__(self, rebuild=False):
        self.print_intro()
        self.input_key(rebuild)
        self.write_dict_to_file()
        self.encrypt_secret()
        print()

    def input_key(self, rebuild):
        # Secret config - docker
        self.dict_key_make(config_secret_common, 'docker')
        self.input_dict_value(
            msg='DockerImage Created Root Name',
            dic=config_secret_common['docker'],
            key='createdImageRootName'
        )
        self.input_dict_value(
            msg='DockerImage Maintainer Email',
            dic=config_secret_common['docker'],
            key='maintainer'
        )

        # Secret config - GitHub
        self.dict_key_make(config_secret_common, 'github')
        self.input_dict_value(
            msg='GitHub username',
            dic=config_secret_common['github'],
            key='username'
        )
        self.input_dict_value(
            msg='GitHub password',
            dic=config_secret_common['github'],
            key='password'
        )

        # Secret config - django
        self.dict_key_make(config_secret_common, 'django')
        self.dict_key_make(config_secret_common['django'], 'default_superuser')
        self.input_dict_value(
            msg='Django default superuser username',
            dic=config_secret_common['django']['default_superuser'],
            key='username'
        )
        self.input_dict_value(
            msg='Django default superuser password',
            dic=config_secret_common['django']['default_superuser'],
            key='password'
        )
        self.input_dict_value(
            msg='Django default superuser email',
            dic=config_secret_common['django']['default_superuser'],
            key='email',
            default='',
        )
        self.dict_key_make(config_secret_local, 'django')
        self.input_dict_value(
            msg='Django allowed hosts (default: ["*"])',
            dic=config_secret_local['django'],
            key='allowed_hosts',
            default=['*', ],
        )

        # Secret config - db
        self.dict_key_make(config_secret_local, 'db')
        db_engine = self.input_dict_value(
            msg='DB Engine (default: django.db.backends.postgresql_psycopg2)',
            dic=config_secret_local['db'],
            key='engine',
            default='django.db.backends.postgresql_psycopg2',
        )
        if 'sqlite' in db_engine:
            sqlite_db_name = os.path.join(BASE_DIR, 'db.sqlite3')
            self.input_dict_value(
                msg='DB Name (default: {})'.format(sqlite_db_name),
                dic=config_secret_local['db'],
                key='name',
                default=sqlite_db_name,
            )
        else:
            self.input_dict_value(
                msg='DB Name (default: api-ios)',
                dic=config_secret_local['db'],
                key='name',
                default='api-ios',
            )
            self.input_dict_value(
                msg='DB Host (default: localhost)',
                dic=config_secret_local['db'],
                key='host',
                default='localhost'
            )
            self.input_dict_value(
                msg='DB Port (default: 5432)',
                dic=config_secret_local['db'],
                key='port',
                default='5432'
            )
            self.input_dict_value(
                msg='DB User',
                dic=config_secret_local['db'],
                key='user',
            )
            self.input_dict_value(
                msg='DB Password',
                dic=config_secret_local['db'],
                key='password',
            )

    @staticmethod
    def write_dict_to_file():
        with open(CONF_SECRET_COMMON_FILE, 'wt') as f:
            f.write(json.dumps(config_secret_common, indent=4, sort_keys=True))
        with open(CONF_SECRET_LOCAL_FILE, 'wt') as f:
            f.write(json.dumps(config_secret_local, indent=4, sort_keys=True))

    @staticmethod
    def encrypt_secret():
        encrypt_command = 'tar cvf secrets.tar .conf_secret &&' \
                          'travis encrypt-file secrets.tar --add &&' \
                          'git add secrets.tar.enc .travis.yml'
        subprocess.run(encrypt_command, shell=True)
        print(' encrypt secret config')

    @staticmethod
    def print_intro():
        intro_string = '=== SettingsBuild ==='
        print(intro_string)

    @staticmethod
    def dict_key_make(dic, key):
        """
        dic에 key에 해당하는 dict가 없을 경우 생성해줌
        :param dic: dict
        :param key: dic에 추가할 dict의 key
        :return:
        """
        if not dic.get(key):
            dic[key] = {}

    @staticmethod
    def input_dict_value(msg, dic, key, default=None):
        """
        아래의 조건동안 dic으로 전달된 dict에 넣을 값을 입력받는다
        매 입력마다 msg의 값을 출력해준다
            1. 해당 키 값이 없거나
            2. 키의 타입이 str이며 양쪽 여백을 없앤 결과(.strip())가 공백인 경우
        :param msg: 어떤 키에 값을 넣을것인지 메시지 출력
        :param dic: 실제로 값을 기록할 dict
        :param key: dict에서 값을 기록할 key
        :param default: 입력되지 않을 경우 기본적으로 넣을 값
        :return: 입력된 값
        """
        while not dic.get(key) or (isinstance(dic[key], str) and dic[key].strip() == ''):
            value = input('{}: '.format(msg)).strip()
            dic[key] = value
            if default and value == '':
                dic[key] = default
        return dic[key]
