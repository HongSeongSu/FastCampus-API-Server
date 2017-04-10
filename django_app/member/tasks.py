import time
from celery.utils.log import get_task_logger

from config.celery import app
from member.models import CeleryTest

logger = get_task_logger(__name__)


@app.task
def member_celery_test():
    logger.info('** CALLING member_celery_task **')
    time.sleep(10)
    CeleryTest.objects.create()
