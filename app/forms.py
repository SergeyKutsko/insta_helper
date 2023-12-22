from django import forms
from .models import UserId


class UserIdForm(forms.ModelForm):

    class Meta:
        model = UserId
        fields = ['url']
