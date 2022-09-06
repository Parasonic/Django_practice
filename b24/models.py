from django.db import models
from django.utils.html import format_html
from django.core.validators import RegexValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import random
from random import randrange


# Create your models here.


class Region(models.Model):
    region = models.CharField(max_length=200, help_text="Введите регион")

    def __str__(self):
        return self.region


class Partner(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название РП")
    code = models.CharField(max_length=8, help_text="Введите код РП")
    region = models.ManyToManyField(Region, help_text="Выберите регион")
    email = models.EmailField()
    webhook = models.CharField(validators=[URLValidator(message='Введите вебхук в формате: https://ds2016.bitrix24.ru/rest/589/bqm4wp9vy3eatlfn/')], max_length=100, blank=True, help_text="Введите вебхук Б24")
    responsible = models.PositiveIntegerField(blank=True, null=True, help_text="ID ответственного сотрудника в Б24")

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.webhook and self.responsible is None:
            raise ValidationError(_('Если подключён Б24, нужно указать ответственного.'))

    def __str__(self):
        return self.title

    def get_regions(self):
        ret = ''
        for i in self.region.all():
            ret += i.region+'<br>'
        print(ret)
        return format_html(ret)


# class Phone(models.Model):
#     name = models.CharField(max_length=50)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
#     last_date = models.DateField(auto_now=False, auto_now_add=True)
#
#     def str(self):
#         return self.phone_number


class DemoRequest(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'. Длина до 15 цифр.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    name = models.CharField(max_length=100)
    email = models.EmailField()
    request_date = models.DateField(auto_now_add=True)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL, help_text="Выберите регион")
    partner = models.ForeignKey(Partner, null=True, on_delete=models.SET_NULL, help_text="Выберите партнёра")
    verification_code = models.BigIntegerField(null=True, default=random.randint(1000, 9999), max_length=4)
    is_verified = models.BooleanField(null=True, default=False)



    def get_partner(self):
        return self.partner

    def __str__(self):
        return self.name