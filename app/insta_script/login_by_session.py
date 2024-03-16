from instagrapi import Client
from scripts.redis_connect import redis_instance
from app.models import InstagramUser


def auto_login(client: Client, pk: str) -> None:
    if redis_instance().exists(pk):
        session_id = redis_instance().hget(pk, 'session_id')
        cl = client.login_by_sessionid(session_id)
    else:
        user = InstagramUser.objects.get(pk=pk)
        client.country = user.country
        client.country_code = int(user.country_code)
        client.locale = user.locale
        client.timezone_offset = user.timezone
        cl = client.login(user.login, InstagramUser.get_password(pk))
        result = client.get_settings()
        redis_instance().hset(pk, 'session_id', result['authorization_data']['sessionid'])
    return cl

