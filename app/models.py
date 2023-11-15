from django.db import models
from instagapi import Client
from scripts.encode import encrypt_value, decrypt_value


class InstagramUser(models.Model):
    login = models.BinaryField(verbose_name="Логін")
    password = models.BinaryField(verbose_name="Пароль")
    login_key = models.BinaryField(verbose_name="Ключ для логіна")
    password_key = models.BinaryField(verbose_name="Ключ для пароля")

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
            self.login, self.login_key = encrypt_value(self.login)
            self.password, self.password_key = encrypt_value(self.password)
            super().save(*args, **kwargs)

    @staticmethod
    def get_login(pk):
        try:
            setting = InstagramUser.objects.get(pk)
        except ObjectDoesNotExist:
            return f"Key {pk} does not exist"
        return decrypt_value(bytes(setting.login_key), bytes(setting.login))

    @staticmethod
    def get_password(pk):
        try:
            setting = InstagramUser.objects.get(pk)
        except ObjectDoesNotExist:
            return f"Key {pk} does not exist"
        return decrypt_value(bytes(setting.password_key), bytes(setting.password))
