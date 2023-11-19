from django.db import models
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
    password = models.BinaryField(verbose_name="Пароль")
    password_key = models.BinaryField(verbose_name="Ключ для пароля")
    main = models.BooleanField(default=False, verbose_name="Головна сторінка")
    follower = models.IntegerField(default=0, verbose_name="Читачі")
    track = models.IntegerField(default=0, verbose_name="Підписники")
    target = models.IntegerField(default=0, verbose_name="Ціль підписників")
    sum = models.IntegerField(default=0, verbose_name="Вартість просування")
    teg = models.ManyToManyField(Teg, verbose_name="Теги")

    class Meta:
        verbose_name = 'Користувач Інстаграма'
        verbose_name_plural = 'Користувачі інтаграма'

    def __str__(self):
        return f'{self.login} {self.password}'

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


