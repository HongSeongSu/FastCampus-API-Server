import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):  # 1
        for arg in sys.argv:  # 2
            if 'liveserver' in arg:  # 3
                cls.server_url = 'http://' + arg.split('=')[1]  # 4
                return  # 5
        super().setUpClass()  # 6
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
