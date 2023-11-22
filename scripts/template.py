from app.models import Template

settings = {
    'FIRST_MESSAGE': 'Hello'
}


def run():
    for key, value in settings.items():
        Template.objects.create(key=key, value=value)