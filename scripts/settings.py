from app.models import SystemSetting

settings = {
    'AMOUNT_FOLLOWERS': 100
}


def run():
    for key, value in settings.items():
        SystemSetting.objects.create(key=key, value=value)