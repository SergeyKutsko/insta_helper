# Generated by Django 4.2.8 on 2023-12-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_instagramuser_message_userid_message_listname'),
    ]

    operations = [
        migrations.AddField(
            model_name='limit',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Опис'),
        ),
        migrations.AddField(
            model_name='systemsetting',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Опис'),
        ),
    ]
