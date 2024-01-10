from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from instagrapi import Client
from scripts.encode import encrypt_value, decrypt_value
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from scripts.redis_connect import redis_instance


class InstagramUser(models.Model):
    class Age(models.TextChoices):
        FIRST = 'FIRST', '0 - 21'
        SECOND = 'SECOND', '21 - 90'
        THIRD = 'THIRD', '90 - 180'
        LAST = 'LAST', '180+'

    login = models.CharField(max_length=255, validators=[MaxLengthValidator(limit_value=255)],
                             verbose_name="Логін")
    password = models.CharField(max_length=255, validators=[MaxLengthValidator(limit_value=255)], default='****',
                                verbose_name="Пароль")
    password_secure = models.BinaryField(verbose_name='Засекречений пароль', null=True, blank=True)
    password_key = models.BinaryField(verbose_name="Ключ для пароля", null=True, blank=True)
    age = models.CharField(max_length=6, default=Age.FIRST, choices=Age.choices,
                           verbose_name='Вік профілю (дні)')
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    system = models.BooleanField(default=False, verbose_name='Системний акаунт')
    country = models.CharField(max_length=255, validators=[MaxLengthValidator(limit_value=255)],
                               verbose_name='Країна для акаунта', default='UA')
    country_code = models.IntegerField(default=380, verbose_name='Телефонний код для країни')
    locale = models.CharField(max_length=255, validators=[MaxLengthValidator(limit_value=255)],
                              verbose_name='Локація для країни', default='uk_UA')
    timezone = models.IntegerField(default=7200, verbose_name='Таймзона для країни')

    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Акаунт'
        verbose_name_plural = 'Акаунти'

    def __str__(self):
        return f'{self.login}'

    def save(self, *args, **kwargs):
        try:
            cl = Client()
            cl.country = self.country
            cl.country_code = self.country_code
            cl.locale = self.locale
            cl.timezone_offset = self.timezone
            cl.login(self.login, self.password)
            result = cl.get_settings()
        except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException) as e:
            raise ValidationError('Incorrect tributes') from e
        else:
            self.password_secure, self.password_key = encrypt_value(self.password)
            self.password = ' '
            super().save(*args, **kwargs)
            saved_pk = self.pk
            redis_instance().hset(saved_pk, 'session_id', result['authorization_data']['sessionid'])

    @staticmethod
    def get_password(pk):
        try:
            setting = InstagramUser.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return f"Key {pk} does not exist"
        return decrypt_value(bytes(setting.password_key), bytes(setting.password_secure))


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
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Опис')
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    account = models.ForeignKey(InstagramUser, null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name="Акаунт")

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблони'

    def __str__(self):
        return self.value


class SystemSetting(models.Model):
    key = models.CharField(max_length=255, verbose_name="Ключ")
    value = models.CharField(max_length=255, verbose_name="Значення")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Опис")
    user = models.ForeignKey(User, null=True, blank=True,
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
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")

    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Дані розсилки'
        verbose_name_plural = 'Дані розсилки'


class UserId(models.Model):
    url = models.CharField(max_length=255, verbose_name="Силка на сторінку")
    page_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отримувач")
    user = models.ForeignKey(User,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Список користувачів'
        verbose_name_plural = 'Список користувачів'
        unique_together = ['url', 'user']


class ListName(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва списку", unique=True)
    user_list = models.ManyToManyField(UserId, verbose_name="Список користувачів")
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name="Користувач")
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'

    def __str__(self):
        return self.name


class Followers(models.Model):
    page_id = models.CharField(max_length=255, validators=[MaxLengthValidator(limit_value=255)],
                               verbose_name="Номер сторінки")
    account = models.ForeignKey(User, null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name="Користувач")

    class Meta:
        verbose_name = 'Послідовувач'
        verbose_name_plural = 'Послідовувачі'
        unique_together = ['page_id', 'account']

    def __str__(self):
        return self.page_id


class MessageTemplate(models.Model):
    key = models.CharField(max_length=255, verbose_name="Ключ")
    value = models.TextField(verbose_name="Текст повідомлення")
    user = models.ForeignKey(User,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")

    class Meta:
        verbose_name = 'Шаблон повідомлень'
        verbose_name_plural = 'Шаблони повідомлень'


class SendMessageByUrl(models.Model):
    url = models.CharField(max_length=255, verbose_name="Лінк на сторінку")
    direct_message = models.ForeignKey(MessageTemplate,
                                       on_delete=models.CASCADE,
                                       verbose_name="Текст повідомлення")
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")
    accounts = models.ManyToManyField(InstagramUser,
                                      verbose_name="Аккаунти")

    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Розсилка по аккаунту'
        verbose_name_plural = 'Розсилки по аккаунту'


class SendMessageByList(models.Model):
    lists = models.ManyToManyField(ListName, verbose_name="Списки")
    direct_message = models.ForeignKey(MessageTemplate,
                                       on_delete=models.CASCADE,
                                       verbose_name="Текст повідомлення")
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")
    accounts = models.ManyToManyField(InstagramUser,
                                      verbose_name="Аккаунти")

    created_at = models.DateTimeField(editable=False, auto_now_add=True,
                                      verbose_name='Створено')

    class Meta:
        verbose_name = 'Розсилка по списку'
        verbose_name_plural = 'Розсилки по списку'




