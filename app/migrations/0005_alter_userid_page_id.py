# Generated by Django 4.1.8 on 2023-12-12 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_systemsetting_account_systemsetting_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userid',
            name='page_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отримувач'),
        ),
    ]
