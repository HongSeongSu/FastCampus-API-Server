import time

from ..config.celery import app


@app.task(bind=True)
def config_celery_test():
    time.sleep(3)
    print('call celery_test()')
