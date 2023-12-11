from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from instagrapi import Client
from scripts.encode import encrypt_value, decrypt_value
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user.username) if self.user else ''

    @classmethod
    def get_user(cls, pk):
        return cls.objects.get(id=pk)

    class Meta:
        verbose_name = 'Власники'
        verbose_name_plural = 'Власники'


class InstagramUser(models.Model):
    class Age(models.TextChoices):
        FIRST = 'FIRST', '0 - 21'
        SECOND = 'SECOND', '21 - 90'
        THIRD = 'THIRD', '90 - 180'
        LAST = 'LAST', '180+'

    login = models.CharField(max_length=255, validators=[MaxValueValidator(255), ],
                             verbose_name="Логін")
    password = models.BinaryField(verbose_name="Пароль")
    password_key = models.BinaryField(verbose_name="Ключ для пароля", null=True, blank=True)
    age = models.CharField(max_length=6, default=Age.FIRST, choices=Age.choices,
                           verbose_name='Вік профілю (дні)')
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")

    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Користувач Інстаграма'
        verbose_name_plural = 'Користувачі інтаграма'

    def __str__(self):
        return f'{self.login}'

    def save(self, *args, **kwargs):
        try:
            cl = Client()
            cl.login(self.login, self.password)
        except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException) as e:
            raise ValidationError('Incorrect tributes') from e
        else:
            self.password, self.password_key = encrypt_value(self.password)
            super().save(*args, **kwargs)

    @staticmethod
    def get_password(pk):
        try:
            setting = InstagramUser.objects.get(pk)
        except ObjectDoesNotExist:
            return f"Key {pk} does not exist"
        return decrypt_value(bytes(setting.password_key), bytes(setting.password))


class Limit(models.Model):
    name = models.CharField(max_length=255, verbose_name="Імя")
    limit = models.IntegerField(verbose_name="Обмеження")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Опис")

    def __str__(self):
        return str(self.limit)

    class Meta:
        verbose_name = 'Обмеження інстаграма'
        verbose_name_plural = 'Обмеження інстаграма'

    @staticmethod
    def get_limit(name, default):
        limit_value = Limit.objects.filter(name=name).values('limit').first()
        if limit_value is not None:
            return int(limit_value.get('limit', default))
        return None


class Template(models.Model):
    key = models.CharField(max_length=255, verbose_name="Ключ")
    value = models.TextField(verbose_name="Шаблон відповіді")

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблони'

    def __str__(self):
        return self.value


class SystemSetting(models.Model):
    key = models.CharField(max_length=255, verbose_name="Ключ")
    value = models.CharField(max_length=255, verbose_name="Значення")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Опис")
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    account = models.ForeignKey(InstagramUser, null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name="Аккаунт")

    class Meta:
        verbose_name = 'Налаштування'
        verbose_name_plural = 'Налаштування'

    def __str__(self):
        return self.value

    @staticmethod
    def get_value(key, pk, default=100):
        try:
            value = SystemSetting.objects.get(key=key, account=pk)
        except ObjectDoesNotExist:
            return default
        return value


class Message(models.Model):
    following = models.BooleanField(default=False, verbose_name="Конкурент")
    recipient = models.CharField(max_length=255, verbose_name="Отримувач")
    direct_message = models.TextField(verbose_name="Текст повідомлення")
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")

    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Дані розсилки'
        verbose_name_plural = 'Дані розсилки'


class UserId(models.Model):
    url = models.CharField(max_length=255, verbose_name="Силка на сторінку")
    page_id = models.CharField(max_length=255, verbose_name="Отримувач")
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Список користувачів'
        verbose_name_plural = 'Список користувачів'


class ListName(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва списку")
    user_list = models.ManyToManyField(UserId, verbose_name="Список користувачів")
    user = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'


class Followers(models.Model):
    page_id = models.CharField(max_length=255, verbose_name="Номер сторінки")
    account = models.ForeignKey(CustomUser, null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name="Користувач")

    class Meta:
        verbose_name = 'Послідовувач'
        verbose_name_plural = 'Послідовувачі'

    def __str__(self):
        return self.page_id




