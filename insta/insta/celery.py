from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta.settings')

app_insta = Celery('insta')

app_insta.config_from_object('django.conf:settings', namespace='CELERY')

app_insta.autodiscover_tasks()