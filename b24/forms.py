from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime  # for checking renewal date range.


class DemoForm(ModelForm):

    class Meta:
        model = DemoRequest
        fields = ('phone_number', 'name', 'email', 'region')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control', 'title': 'Ваш регион'}),
        }
        help_texts = {'region': None, }

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        try:
            q = DemoRequest.objects.get(phone_number__exact=data)
            print(q.is_verified)
            if q.is_verified is True:
                raise ValidationError('Данный номер телефона уже использовался ранее.')

        except ObjectDoesNotExist:
            print('Не найдена заявка с таким номером')
            return data

        return data


class VerificationForm(ModelForm):

    class Meta:
        model = DemoRequest
        fields = ('verification_code',)
        widgets = {
            'verification_code': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {'verification_code': 'Ведите код полученный по СМС', }


    # def clean_phone_number(self):
    #     data = self.cleaned_data['phone_number']
    #     q = DemoRequest.objects.filter(phone_number=data)
    #     print(q)
    #     # Проверка на наличие заявок с данным номером
    #     if q:
    #         raise ValidationError('Данный номер телефона уже использовался ранее.')
    #
    #     return data
