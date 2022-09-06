# Generated by Django 4.0.4 on 2022-07-12 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b24', '0003_partner_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='demorequest',
            name='is_verified',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demorequest',
            name='verification_code',
            field=models.BigIntegerField(default=0, max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='demorequest',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть в формате: '+999999999'. Длина до 15 цифр.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]