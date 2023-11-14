# Generated by Django 4.2 on 2023-11-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.BinaryField(verbose_name='Логін')),
                ('password', models.BinaryField(verbose_name='Пароль')),
                ('login_key', models.BinaryField(verbose_name='Ключ для логіна')),
                ('password_key', models.BinaryField(verbose_name='Ключ для пароля')),
            ],
            options={
                'verbose_name': 'Користувач Інстаграма',
                'verbose_name_plural': 'Користувачі інтаграма',
            },
        ),
    ]
