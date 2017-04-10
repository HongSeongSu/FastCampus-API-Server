import logging

from django.http import HttpResponse

from member.tasks import member_celery_test

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def index(request):
    return HttpResponse('FastCampus iOS API Server')


def celery_test(request):
    logger.info('celery_test')
    member_celery_test.delay()
    return HttpResponse('call member_celery_test()')
