from insta.celery import app_insta
from celery import shared_task


@shared_task
def my_celery_task():
    print("Hello from Celery!")

