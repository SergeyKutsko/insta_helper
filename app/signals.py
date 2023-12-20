from .models import InstagramUser, Template, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .vars import welcome_default_value, des_welcome
# from insta.tasks import get_user_id_by_teg_


# @receiver(post_save, sender=Teg)
# def run_celery_task_on_teg_creation(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         get_user_id_by_teg_.delay(instance.name, instance.id)


@receiver(post_save, sender=InstagramUser)
def instagram_user_saved(sender, instance, created, **kwargs):
    if created:
        for i in range(1, 16):
            Template.objects.create(key=f'WELCOME_{i}',
                                    value=welcome_default_value,
                                    description=des_welcome,
                                    user=instance.user,
                                    account=instance,
                                    )
