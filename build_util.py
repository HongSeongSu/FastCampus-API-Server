import json
import os
import re
import subprocess

from collections import OrderedDict
from pprint import pprint

ROOT_DIR = os.path.dirname(__file__)
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

__all__ = (
    'DockerBuild',
    'dict_key_make',
    'input_dict_value',
)


class DockerCategory:
    def __init__(self, base_image_name, order, title, path, options=None):
        self.base_image_name = base_image_name
        self.order = order
        self.title = title
        self.path = path
        self.options = []

        re_compile_option = re.compile(r'^([0-9]+)\.(.*)\.docker')

        option_listdir = os.listdir(self.path)
        # 각 카테고리(00.template, 01.base...)내의 파일들을 순회
        for option in option_listdir:
            # 03.extra의 01.debug, 01.production...도 순회
            cur_option_order = re_compile_option.search(option).group(1)
            # Option인스턴스의 order가 cur_option_order(00, 01등)과 같은 Option이 self.options리스트 목록에 없을 경우 새로 만들어 줌
            if not any(option.order == cur_option_order for option in self.options):
                cur_option = DockerCategoryOption(category=self, order=cur_option_order)
                self.options.append(cur_option)
            # 같은 옵션번호를 가질 경우 cur_option은 같은 DockerCategoryOption객체를 사용
            cur_option = next(
                (option for option in self.options if option.order == cur_option_order), None)
            # 파일 하나하나가 서브옵션이므로 각 루프마다 서브옵션을 생성, 추가
            cur_sub_option = DockerCategorySubOption(
                parent_option=cur_option,
                order=cur_option_order,
                title=re_compile_option.search(option).group(2)
            )
            cur_option.sub_options.append(cur_sub_option)

    def __str__(self):
        ret = 'DockerCategory({}.{})\n'.format(self.order, self.title)
        items = {
            'order': self.order,
            'title': self.title,
            'path': self.path,
            'options': self.options
        }
        for k, v in items.items():
            ret += '  {:10}: {}\n'.format(k, v)
        ret = ret[:-1]
        return ret

    @property
    def is_require_select_option(self):
        for option in self.options:
            if option.is_require_select_option:
                return True
        return False

    @property
    def unique_options(self):
        if self.is_require_select_option:
            raise Exception('require option select')
        return [sub_option for option in self.options for sub_option in option.sub_options]

    def select_options(self):
        for option in self.options:
            option.select_sub_option()


class DockerCategoryOption:
    def __init__(self, category, order, options=None):
        self.category = category
        self.order = order
        self.sub_options = options if options else []
        self.selected_sub_option = None

    def __repr__(self):
        return 'Option(Category:[{}], Order:[{}])'.format(
            self.category.title,
            self.order,
        )

    @property
    def is_require_select_option(self):
        if len(self.sub_options) > 1:
            return True
        return False

    @property
    def unique_sub_option(self):
        if self.is_require_select_option:
            raise Exception('require select sub option')
        else:
            return self.sub_options[0]

    def select_sub_option(self):
        self.selected_sub_option = None
        if self.is_require_select_option:
            select_string = 'Category({}.{})\n - Option({})\n -- SubOption select:\n'.format(
                self.category.order,
                self.category.title,
                self.order
            )
            for index, sub_option in enumerate(self.sub_options):
                select_string += '  {}.{}\n'.format(
                    index + 1,
                    sub_option.title
                )
            select_string = select_string[:-1]
            while True:
                print(select_string)
                selected_sub_option_index = input('  > Select SubOption: ')
                try:
                    selected_sub_option = self.sub_options[int(selected_sub_option_index) - 1]
                    self.selected_sub_option = selected_sub_option
                    print('')
                    break
                except ValueError as e:
                    print('  ! Input value error ({})\n'.format(e))
                except IndexError as e:
                    print('  ! Selected SubOption index is not valid ({})\n'.format(e))

        else:
            self.selected_sub_option = self.unique_sub_option
            # print('Don\'t need select SubOption. This Option has unique SubOption')
        return self.selected_sub_option


class DockerCategorySubOption:
    def __init__(self, parent_option, order, title):
        self.parent_option = parent_option
        self.order = order
        self.title = title

    def __repr__(self):
        return self.info

    @property
    def info(self):
        return '{}-{}-{}-{}'.format(
            self.parent_option.category.base_image_name,
            self.parent_option.category.title,
            self.parent_option.order,
            self.title
        )

    @property
    def path(self):
        return '{}/{}.{}.docker'.format(
            self.parent_option.category.path,
            self.order,
            self.title
        )


class DockerBuild:
    def __init__(self, conf_dir):
        self.categories = []
        self.root_image_name = config_docker['createdImageRootName']
        self.start_image = None
        self.end_image = None
        re_compile_category = re.compile(r'^([0-9]+)\.(.*)')
        docker_conf_listdir = os.listdir(conf_dir)

        for category in docker_conf_listdir:
            if os.path.isdir(os.path.join(conf_dir, category)):
                cur_category = DockerCategory(
                    base_image_name=self.root_image_name,
                    order=re_compile_category.search(category).group(1),
                    title=re_compile_category.search(category).group(2),
                    path=os.path.join(CONF_DOCKER_DIR, category),
                )
                self.categories.append(cur_category)

        self.print_intro()
        self.set_options()
        self.set_start_image()
        self.set_end_image()
        self.make_dockerfiles()

    @staticmethod
    def print_intro():
        intro_string = '=========================\n'
        intro_string += '=== DockerBuild Start ===\n'
        intro_string += '========================='
        print(intro_string)

    def set_options(self):
        for category in self.categories:
            category.select_options()

    @property
    def selected_options(self):
        """
        각 카테고리(template, base, common, extra)의 
        옵션 (00, 01, 02...등)에
        선택한 서브옵션 (03.extra - 01 - debug or production)들로 이루어진 리스트를 리턴
        서브옵션이 선택되지 않았을 경우 None이 원소로 반환됨
        :return: list(DockerCategorySubOption)
        """
        return [option.selected_sub_option for category in self.categories for option in
                category.options]

    @property
    def is_selected_all_sub_options(self):
        """
        모든 카테고리의 옵션에 대해 서브옵션을 선택했는지 여부 반환
        :return: Bool, 모든 서브옵션을 선택했는지
        """
        return all(self.selected_options)

    def set_start_image(self):
        select_string = 'Select start image:\n'
        select_string += '  {}.{}\n'.format(
            0, config_docker['imageNameRoot'],
        )
        for index, option in enumerate(self.selected_options):
            select_string += '  {}.{}\n'.format(
                index + 1,
                option.info
            )
        select_string = select_string[:-1]
        while True:
            print(select_string)
            selected_option_index = input(
                '  > Select image number (default: {}.{}): '.format(
                    0, config_docker['imageNameRoot']
                )
            )
            try:
                if selected_option_index == '' or selected_option_index == '0':
                    self.start_image = None
                else:
                    self.start_image = self.selected_options[int(selected_option_index) - 1]
                print('')
                break
            except ValueError as e:
                print('  ! Input value error ({})\n'.format(e))
            except IndexError as e:
                print('  ! Selected SubOption index is not valid ({})\n'.format(e))

    def set_end_image(self):
        start_index = self.selected_options.index(self.start_image) if self.start_image else 0
        select_string = 'Select end image:\n'
        for index, option in enumerate(self.selected_options):
            if index < start_index:
                continue
            select_string += '  {}.{}\n'.format(
                index + 1,
                option.info
            )
        select_string = select_string[:-1]
        while True:
            print(select_string)
            default_index = len(self.selected_options) - 1
            selected_option_index = input(
                '  > Select image number (default: {}.{}): '.format(
                    default_index + 1,
                    self.selected_options[default_index].info
                )
            )
            try:
                if selected_option_index == '':
                    selected_option_index = default_index + 1
                self.end_image = self.selected_options[int(selected_option_index) - 1]
                print('')
                break
            except ValueError as e:
                print('  ! Input value error ({})\n'.format(e))
            except IndexError as e:
                print('  ! Selected SubOption index is not valid ({})\n'.format(e))

    def make_dockerfiles(self):
        start_index = self.selected_options.index(self.start_image) if self.start_image else None
        end_index = self.selected_options.index(self.end_image)
        root_image_name = config_docker['imageNameRoot']

        template = open(os.path.join(CONF_DOCKER_DIR, 'template.docker')).read()
        print('== Make Dockerfiles ==')
        for index, option in enumerate(self.selected_options):
            if (start_index and index < start_index) or index > end_index:
                continue
            file_name = 'Dockerfile.{}.{}.{}.{}'.format(
                option.parent_option.category.order,
                option.parent_option.category.title,
                option.parent_option.order,
                option.title)
            print(file_name)
            prev_image = self.selected_options[index - 1].info if index > 0 else root_image_name
            cur_template = template.format(
                from_image=prev_image,
                maintainer=config_secret_common['docker']['maintainer'],
                content=open(os.path.join(option.path), 'rt').read(),
            )
            open(os.path.join(ROOT_DIR, file_name), 'wt').write(cur_template)
            build_command_template = 'docker build . -t {name} -f {dockerfile_name}'
            build_command = build_command_template.format(
                name=option.info,
                dockerfile_name=file_name
            )
            subprocess.run(build_command, shell=True)


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


def make_categories():
    """
    빌드용 카테고리 생성
    :return:
    """
    # make options from docker_conf
    re_compile_category = re.compile(r'^([0-9]+)\.(.*)')
    re_compile_option = re.compile(r'^([0-9]+)\.(.*)\.docker')
    docker_conf_listdir = os.listdir(CONF_DOCKER_DIR)
    categories = [
        {
            'order': re_compile_category.search(category).group(1),
            'title': re_compile_category.search(category).group(2),
            'path': os.path.join(CONF_DOCKER_DIR, category),
            'options': OrderedDict(),
        }
        for category in docker_conf_listdir
        if os.path.isdir(os.path.join(CONF_DOCKER_DIR, category))
    ]
    # for k, v in categories:
    #     print(k, v)

    root_image_name = config_docker['createdImageRootName']
    from_image = config_docker['imageNameRoot']
    for category in categories:
        option_listdir = os.listdir(category['path'])
        for option in option_listdir:
            cur_option_order = re_compile_option.search(option).group(1)
            if cur_option_order not in category['options']:
                category['options'][cur_option_order] = []

            cur_option = {
                'cur_image': '{}-{}-{}-{}'.format(
                    root_image_name,
                    category['title'],
                    cur_option_order,
                    re_compile_option.search(option).group(2),
                ),
                'order': cur_option_order,
                'title': re_compile_option.search(option).group(2),
                'path': os.path.join(category['path'], option),
            }
            category['options'][cur_option_order].append(cur_option)

    pprint(categories)
    return categories


def get_start_image_name():
    """
    시작할 이미지명을 리턴
    :return:
    """
    categories = make_categories()
    while True:
        print('\n어떤 카테고리부터 시작하시겠습니까?')
        for index, category in enumerate(categories):
            print('  {}. {}'.format(
                index,
                category['title']
            ))
        try:
            category_index = int(input('입력(default: 0): '))
            selected_category = categories[category_index]

            previous_image_name = None
            previous_category = categories[category_index - 1]
            if category_index != 0 and len(previous_category['options']) > 1:
                while True:
                    print('이전 카테고리에서 시작할 이미지를 선택해주세요')
                    cur_index = 1
                    item_list = []
                    for index, sub_options in enumerate(previous_category['options'].values()):
                        for sub_index, sub_option in enumerate(sub_options):
                            print('  {}. {}'.format(
                                cur_index,
                                sub_option['cur_image']
                            ))
                            cur_index += 1
                            item_list.append({
                                'index': index,
                                'sub_index': sub_index
                            })
                    item_index = int(input('입력: '))
                    try:
                        item = item_list[item_index - 1]
                        selected_sub_option = \
                            list(previous_category['options'].values())[item['index']][
                                item['sub_index']]
                        previous_image_name = selected_sub_option['cur_image']
                        break
                    except Exception as e:
                        print(e)
            elif category_index != 0 and len(previous_category['options']) == 1:
                previous_image_name = list(previous_category['options'].values())[0][0]['cur_image']

            print('시작 이미지명 : {}'.format(previous_image_name))
            return previous_image_name
        except Exception as e:
            print(e)
            # except ValueError:
            #     print(' 예외 - 정수값을 입력해주세요')
            # except IndexError:
            #     print(' 예외 - 선택가능 범위값을 입력해주세요')


def select_images():
    categories = make_categories()
