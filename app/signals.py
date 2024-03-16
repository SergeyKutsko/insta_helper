from .models import InstagramUser, Template, User, MessageTemplate, \
    Task, SendMessageByList, SendMessageByUrl, NameMessageTemplate, AccountCounterTasks
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .vars import welcome_default_value, des_welcome, m_template_value_default
from insta.tasks import create_task_url, create_task_list


@receiver(post_save, sender=InstagramUser)
def instagram_user_saved(sender, instance, created, **kwargs):
    if created:
        AccountCounterTasks.objects.create(account=instance,
                                           user=instance.user)
        for i in range(1, 31):
            Template.objects.create(key=f'WELCOME_{i}',
                                    value=welcome_default_value,
                                    description=des_welcome,
                                    user=instance.user,
                                    account=instance,
                                    )


@receiver(post_save, sender=SendMessageByUrl)
def create_task_before_save(sender, instance, created, **kwargs):
    if created:
        create_task_url.apply_async(args=[instance.id], countdown=1800)


@receiver(post_save, sender=SendMessageByList)
def create_task_before_save(sender, instance, created, **kwargs):
    if created:
        create_task_list.apply_async(args=[instance.id], countdown=1800)
