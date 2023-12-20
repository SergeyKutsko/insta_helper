from django import forms
from .models import UserId


class UserIdForm(forms.ModelForm):

    class Meta:
        model = UserId
        fields = ['url']


class SendMessageByUrl(forms.ModelForm):
    url = forms.CharField(max_length=255)

    class Meta:
        labels = {'field_name': 'Розсилка по аккаунту', 'url': 'Вставте силку на сторінку'}


