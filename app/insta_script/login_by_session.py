from instagrapi import Client
from scripts.redis_connect import redis_instance
from app.models import InstagramUser, SystemSetting


def auto_login(client: Client, pk: str) -> None:
    if redis_instance.exists(pk):
        session_id = redis_instance().hget(pk, 'session_id')
        client.login_by_sessionid(session_id)
    else:
        user = InstagramUser.objects.get(pk=pk)
        client.country = SystemSetting.get_value('COUNTRY', pk)
        client.country_code = int(SystemSetting.get_value('COUNTRY_CODE', pk))
        client.locale = SystemSetting.get_value('LOCALE', pk)
        client.timezone_offset = int(SystemSetting.get_value('TIMEZONE_OFFSET', pk))
        client.login(user.login, InstagramUser.get_password(pk))
        result = client.get_session()
        redis_instance().hset(pk, 'session_id', result['authorization_data']['sessionid'])

