from django.db import models


class InstagramUser(models.Model):
    login = models.BinaryField(verbose_name="Логін")
    password = models.BinaryField(verbose_name="Пароль")
    login_key = models.BinaryField(verbose_name="Ключ для логіна")
    password_key = models.BinaryField(verbose_name="Ключ для пароля")

    class Meta:
        verbose_name = 'Користувач Інстаграма'
        verbose_name_plural = 'Користувачі інтаграма'

    def __str__(self):
        return f'{self.login} {self.value}'
