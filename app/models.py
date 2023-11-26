from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from instagrapi import Client
from scripts.encode import encrypt_value, decrypt_value


class Teg(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class InstagramUser(models.Model):
    name = models.CharField(max_length=255, verbose_name="Імя", null=True, blank=True)
    second_name = models.CharField(max_length=255, verbose_name="Прізвище", null=True, blank=True)
    login = models.CharField(max_length=255, verbose_name="Логін")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    main = models.BooleanField(default=False, verbose_name="Головна сторінка")
    system = models.BooleanField(default=False, verbose_name="Системна сторінка")
    uniq_following = models.BooleanField(default=False, verbose_name="Унікальність підписок")
    active = models.BooleanField(default=True, verbose_name="Активувати")
    follower = models.IntegerField(default=0, verbose_name="Читачі")
    track = models.IntegerField(default=0, verbose_name="Підписники")
    target = models.IntegerField(default=0, verbose_name="Ціль підписників")
    teg = models.ManyToManyField(Teg, verbose_name="Теги")

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
            super().save(*args, **kwargs)

    @staticmethod
    def get_password(pk):
        try:
            setting = InstagramUser.objects.get(pk)
        except ObjectDoesNotExist:
            return f"Key {pk} does not exist"
        return setting.login, setting.password


class Limit(models.Model):
    name = models.CharField(max_length=255, verbose_name="Імя")
    limit = models.IntegerField(verbose_name="Обмеження")

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


class Income(models.Model):
    class Currency(models.TextChoices):
        UAH = 'UAH', 'Гривня',
        USD = 'USD', 'Долар',
        EUR = 'EUR', 'Євро',

    class Meta:
        verbose_name = 'Дохід'
        verbose_name_plural = 'Доходи'

    sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Вартість просування")
    currency = models.CharField(max_length=3, default=Currency.UAH, choices=Currency.choices,
                                verbose_name='Валюта')
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE, verbose_name="Інстаграм користувач")
    created_at = models.DateTimeField(editable=False, auto_now_add=True,
                                      verbose_name='Додано дохід')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено')

    def __str__(self):
        return self.currency


class UserID(models.Model):
    user_id = models.IntegerField(verbose_name="Номер сторінки в інстаграмі")
    teg = models.ForeignKey(Teg, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        verbose_name = 'Індифікатор користувачів по тегу'
        verbose_name_plural = 'Індифікатори користувачів по тегу'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'teg'], name='unique_user_teg')
        ]

    def __str__(self):
        return self.teg

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(f'Saving error: customer with this ID and tag is already active. {e}')


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

    class Meta:
        verbose_name = 'Налаштування'
        verbose_name_plural = 'Налаштування'

    def __str__(self):
        return self.value

    @staticmethod
    def get_value(key, default=100):
        try:
            value = SystemSetting.objects.get(key=key)
        except ObjectDoesNotExist:
            return default
        return value

