# from .models import Teg
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from insta.tasks import get_user_id_by_teg_


# @receiver(post_save, sender=Teg)
# def run_celery_task_on_teg_creation(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         get_user_id_by_teg_.delay(instance.name, instance.id)