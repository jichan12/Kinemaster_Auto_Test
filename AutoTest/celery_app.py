#celery_app.py
from celery import Celery

# Celery 브로커 및 백엔드 설정
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


def make_celery(app):
    celery = Celery(app.import_name, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery