# Generated by Django 4.1.8 on 2023-12-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_sendmessagebyurl_sendmessagebylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listname',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Назва списку'),
        ),
    ]