# celery.py or wherever your Celery app is configured

from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busstation.settings')

app = Celery('busstation')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'
