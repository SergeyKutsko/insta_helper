from insta.celery import app_insta
from celery import shared_task
from app.models import InstagramUser, SystemSetting
from app.insta_script.login import login_user
from app.insta_script.tegs import get_user_pk_by_tag
from app.insta_script.users import follow, unfollow
from instagrapi import Client
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from app.insta_script.variables import delay
from app.insta_script.login_by_session import auto_login
import logging
import os
from django.db import IntegrityError
import random
from .vars import welcome_default_value


logger = logging.getLogger(__name__)


def get_template(account_id):
    user = InstagramUser.objects.get(id=account_id)
    user_id = user.id
    while True:
        numbers = random.randint(1, 15)
        template = Template.objects.filter(key=f'WELCOME_{numbers}',
                                           user=user_id,
                                           account=account_id)
        if template is not None and template != welcome_default_value:
            break

    return template


def add_follower(page_id, account):
    try:
        follower = Followers.objects.create(page_id=page_id, account=account)
        follower.save()
        return
    except IntegrityError:
        return


def create_queue_and_worker(queue_name):
    if queue_name not in app_insta.conf.task_queues:
        app_insta.conf.task_queues.append(queue_name)

        # Create worker with new queue
        worker_cmd = f'celery -A app_insta worker -Q {queue_name} -l info'
        os.system(worker_cmd)

        logger.info(f'Queue {queue_name} and worker have been created.')
    else:
        logger.info(f'Queue {queue_name} and worker have created')


@app_insta.task()
def add_followers_to_instagram_user(account_id):
    create_queue_and_worker.delay(queue_name=account_id)
    cl = Client()
    auto_login(cl, str(account_id))
    pk_instagram_pages = list(cl.account_info().dict()['pk'])

    existing_followers = Followers.objects.filter(account=account_id, page_id__in=pk_instagram_pages)

    unconfirmed_followers = list(set(pk_instagram_pages) - set(existing_followers.values_list('page_id', flat=True)))
    if unconfirmed_followers:
        template = get_template(account_id)
        unconfirmed_followers = [int(i) for i in unconfirmed_followers]
        cl.direct_send(text=template, user_ids=unconfirmed_followers)
        for page_id in unconfirmed_followers:
            add_follower(page_id, account)


# @app_insta.task
# def get_all_teg():
#     users = UserID.objects.all()
#     for user in users:
#         get_user_id_by_teg_.delay(user, user.id)
#
#
# @app_insta.task
# def get_user_id_by_teg_( teg_name, teg_id):
#     try:
#         user = InstagramUser.objects.get(system=True)
#     except ObjectDoesNotExist:
#         return
#
#     cl = login_user(user.pk, user.login, user.password)
#     users_pk = get_user_pk_by_tag(cl, teg_name, SystemSetting.get_value('AMOUNT_FOLLOWERS'))
#     if users_pk:
#         user_objects = [UserID(user_id=user, teg_id=teg_id) for user in users_pk]
#         UserID.objects.bulk_create(user_objects)
#
#
# @app_insta.task
# def get_all_active_user():
#     active_users = InstagramUser.objects.filter(
#         Q(active=True) & Q(system=False) & Q(main=False)
#     )
#
#     if active_users is None:
#         return
#     for user in active_users:
#         user_tags_pk = list(user.teg.values_list('pk', flat=True))
#         if user_tags_pk:
#             follow_to_user.delay(user.pk, user.login, user.password, user_tags_pk)
#
#
# @app_insta.task
# def follow_to_user(user_pk, login, password, user_tags_names):
#     cl = login_user(str(user_pk), login, password)
#     for pk in user_tags_names:
#         user_ids = UserID.objects.filter(teg=pk).values_list('user_id', flat=True)
#         for user_id in user_ids:
#             follow(cl, str(user_id))
#
#
# @app_insta.task
# def get_all_active_and_uniq_following_users():
#     users = InstagramUser.objects.filter(
#         Q(active=True) & Q(uniq_following=False) & Q(system=False) & Q(main=False)
#     )
#     if users is None:
#         return
#     for user in users:
#         uniq_following_and_followers(user.pk, user.login, user.password)
#
#
# @app_insta.task
# def uniq_following_and_followers(user_pk, login, password):
#     cl = login_user(str(user_pk), login, password)
#     user_id = cl.user_id
#     followers = cl.user_followers(user_id)
#     delay(cl)
#     following = cl.user_following(user_id)
#     unfollowed_users = following - followers
#     for id_user in unfollowed_users:
#         unfollow(cl, str(id_user))



