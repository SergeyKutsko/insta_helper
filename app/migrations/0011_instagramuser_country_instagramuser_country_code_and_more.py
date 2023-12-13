# Generated by Django 4.1.8 on 2023-12-13 17:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_followers_page_id_alter_instagramuser_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramuser',
            name='country',
            field=models.CharField(default='UA', max_length=255, validators=[django.core.validators.MaxLengthValidator(limit_value=255)], verbose_name='Країна для акаунта'),
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='country_code',
            field=models.IntegerField(default=380, verbose_name='Телефонний код для країни'),
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='locale',
            field=models.CharField(default='uk_UA', max_length=255, validators=[django.core.validators.MaxLengthValidator(limit_value=255)], verbose_name='Локація для країни'),
        ),
        migrations.AddField(
            model_name='instagramuser',
            name='timezone',
            field=models.IntegerField(default=7200, verbose_name='Таймзона для країни'),
        ),
    ]