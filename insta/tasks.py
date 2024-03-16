from insta.celery import app_insta
from celery import shared_task
from app.models import InstagramUser, SystemSetting, Limit, Task, SendMessageByUrl, SendMessageByList, ListName, \
    AccountCounterTasks
from celery.schedules import crontab
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
import subprocess
from django.db import connection
from django.db.models import Max
from django.utils import timezone

# from django.db import IntegrityError
import random


logger = logging.getLogger(__name__)


def get_sendmessagebyurl_accounts_records(url_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_sendmessagebyurl_accounts WHERE sendmessagebyurl_id = %s", [url_id])
        records = cursor.fetchall()
        return records


def get_sendmessagebylist_lists_records(lists_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_sendmessagebylist_lists WHERE sendmessagebylist_id = %s", [lists_id])
        records = cursor.fetchall()
        return records


def get_sendmessagebylist_accounts_records(list_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_sendmessagebylist_accounts WHERE sendmessagebylist_id = %s", [list_id])
        records = cursor.fetchall()
        return records

def get_listname_user_records(list_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_listname_user_list WHERE listname_id = %s", [list_id])
        records = cursor.fetchall()
        return records


def get_listname_user_records(list_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_listname_user_list WHERE listname_id = %s", [list_id])
        records = cursor.fetchall()
        return records


@app_insta.task(bind=True)
def create_task_url(context, id_):
    ins = SendMessageByUrl.objects.get(id=id_)
    for i in get_sendmessagebyurl_accounts_records(id_):
        Task.objects.create(
                account=InstagramUser.objects.get(id=i[-1]),
                direct_message=ins.direct_message,
                url=ins.url,
                task_type=Task.TypeTask.URL,
                user=ins.user
        )


@app_insta.task(bind=True)
def create_task_list(context, id_):
    ins = SendMessageByList.objects.get(id=id_)
    lists = get_sendmessagebylist_lists_records(id_)
    accounts = get_sendmessagebylist_accounts_records(id_)
    for i in lists:
        for j in accounts:
            Task.objects.create(
                account=InstagramUser.objects.get(id=j[-1]),
                direct_message=ins.direct_message,
                list=ListName.objects.get(id=i[-1]),
                task_type=Task.TypeTask.LIST,
                user=ins.user
            )


def send_message_by_url(instance_account, instance_task):
    print('Я надсилаю повідомлення')
    response = int(Limit.get_limit('MESSAGE_IN_DIRECT_NO_FOLLOWERS', 35))
    counter = int(AccountCounterTasks.objects.get(
        account=instance_account,
        user=instance_account.user
    ).counter)
    if counter >= response:
        return
    else:
        cl = Client()
        cl.country = instance_account.country
        cl.country_code = int(instance_account.country_code)
        cl.locale = instance_account.locale
        cl.timezone_offset = instance_account.timezone
        cl = cl.login(instance_account.login, InstagramUser.get_password(instance_account.id))
        try:
            url = instance_task.url
            url = url.split('/')[-2]
            user_ = cl.user_info_by_username(url).dict()
        except:
            instance_task.complited = timezone.now()
            instance_task.save()
            return
        print(3)
        res = cl.user_following(user_['pk'], amount=response)
        for i in res.values():
            counter = AccountCounterTasks.objects.get(
                account=instance_account,
                user=instance_account.user
            )
            if int(counter.counter) < response:
                mt = MessageTemplate.objects.filter(key=instance_task.direct_message_id, user_id=instance_account.user)
                my_list = [j.value for j in mt]
                list_length = len(my_list)
                random_index = random.randint(0, list_length - 1)
                time.sleep(random.randint(3, 10))
                cl.direct_send(text=m[random_index],
                               user_ids=[int(i.pk)])
                counter.counter += 1
                counter.save()
                instance_task.complited = timezone.now()
                instance_task.save()
            else:
                return

        print("Я надіслав повідомлення")
        return


def send_message_by_list(instance_account, instance_task):
    response = int(Limit.get_limit('MESSAGE_IN_DIRECT_NO_FOLLOWERS', 35))
    counter = int(AccountCounterTasks.objects.get(
        account=instance_account,
        user=instance_account.user
    ).counter)
    if counter >= response:
        return
    else:
        cl = Client()
        cl.country = instance_account.country
        cl.country_code = int(instance_account.country_code)
        cl.locale = instance_account.locale
        cl.timezone_offset = instance_account.timezone
        cl = cl.login(instance_account.login, InstagramUser.get_password(instance_account.id))
        user_list = get_listname_user_records(instance_task.list_id)
        for i in user_list:
            user_url = UserId.objects.get(id=i[-1])
            try:
                url = user_url.url
                url = url.split('/')[-2]
            except:
                continue
            try:
                user_ = cl.user_info_by_username(url).dict()
                user_url.page_id = user_['pk']
                user_url.save()
            except:
                instance_task.complited = timezone.now()
                instance_task.save()
                return

            counter = AccountCounterTasks.objects.get(
                    account=instance_account,
                    user=instance_account.user
            )
            if int(counter.counter) < response:
                mt = MessageTemplate.objects.filter(key=instance_task.direct_message_id, user_id=instance_account.user)
                my_list = [j.value for j in mt]
                list_length = len(my_list)
                random_index = random.randint(0, list_length - 1)
                time.sleep(random.randint(3, 10))
                cl.direct_send(text=m[random_index],
                               user_ids=[int(user_['pk'])])
                counter.counter += 1
                counter.save()
                instance_task.complited = timezone.now()
                instance_task.save()
            else:
                return

        print("Я надіслав повідомлення")
        return


@app_insta.task()
def run_tasks():
    accounts = InstagramUser.objects.filter(active=True)
    for account in accounts:
        last_completed_task = Task.objects.filter(
            account=account,
            user=account.user,
            complited__isnull=False
        ).aggregate(last_completed=Max('complited'))

        if last_completed_task['last_completed'] is not None:
            last_completed_time = last_completed_task['last_completed']
            now = timezone.now()
            time_difference = now - last_completed_time
            if time_difference.total_seconds() / 3600 > 24:
                account_counter = AccountCounterTasks.objects.get(
                    account=account,
                    user=account.user
                )

                account_counter.counter = 0
                account_counter.save()
        tasks = Task.objects.filter(account=account,
                                    user=account.user,
                                    complited=None)
        for task in tasks:
            print(account)
            if task.task_type == 'LIST':
                send_message_by_list(instance_account=account,
                                     instance_task=task)
            if task.task_type == 'URL':
                send_message_by_url(instance_account=account,
                                    instance_task=task)
            if task.task_type == 'DIRECT':
                pass


@app_insta.on_after_finalize.connect
def run_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*/12'), run_tasks.s())



# @shared_task
# def create_queue_and_worker(queue_name):
#     print('hello')
#     if app_insta.conf.task_queues is None or queue_name not in app_insta.conf.task_queues:
#         print('hello1')
#         if app_insta.conf.task_queues is None:
#             print('hello2')
#
#             app_insta.conf.task_queues = []
#         print('hello3')
#         app_insta.conf.task_queues.append(queue_name)
#         print('hello56')
#         worker_cmd = f'celery -A insta worker -Q {queue_name} -l info'
#         subprocess.Popen(worker_cmd, shell=True)  # Запускаем воркер в новом процессе
#         logger.info(f'Queue {queue_name} and worker have been created.')
#     else:
#         logger.info(f'Queue {queue_name} already exists')



    # print(app_insta.conf.task_queues)
    # if queue_name not in app_insta.conf.task_queues:
    #     app_insta.conf.task_queues.append(queue_name)
    #     # Create worker with new queue
    #     worker_cmd = f'celery -A app_insta worker -Q {queue_name} -l info'
    #     os.system(worker_cmd)
    #
    #     logger.info(f'Queue {queue_name} and worker have been created.')
    # else:
    #     logger.info(f'Queue {queue_name} and worker have created')


# @app_insta.task()
# def add_followers_to_instagram_user(account_id):
#     create_queue_and_worker.delay(queue_name=account_id)
#     cl = Client()
#     auto_login(cl, str(account_id))
#     pk_instagram_pages = list(cl.account_info().dict()['pk'])
#
#     existing_followers = Followers.objects.filter(account=account_id, page_id__in=pk_instagram_pages)
#
#     unconfirmed_followers = list(set(pk_instagram_pages) - set(existing_followers.values_list('page_id', flat=True)))
#     if unconfirmed_followers:
#         template = get_template(account_id)
#         unconfirmed_followers = [int(i) for i in unconfirmed_followers]
#         cl.direct_send(text=template, user_ids=unconfirmed_followers)
#         for page_id in unconfirmed_followers:
#             add_follower(page_id, account_id)
#
#
#
#
# def get_template(account_id):
#     user = InstagramUser.objects.get(id=account_id)
#     user_id = user.id
#     while True:
#         numbers = random.randint(1, 15)
#         template = Template.objects.filter(key=f'WELCOME_{numbers}',
#                                            user=user_id,
#                                            account=account_id)
#         if template is not None and template != welcome_default_value:
#             break
#
#     return template
#
#
# def add_follower(page_id, account):
#     try:
#         follower = Followers.objects.create(page_id=page_id, account=account)
#         follower.save()
#         return
#     except IntegrityError:
#         return
#
#

#
#



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



