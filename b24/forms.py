from django import forms
from django.forms import ModelForm
from .models import *

from django.core.exceptions import ValidationError
import datetime #for checking renewal date range.


class DemoForm(ModelForm):
    # your_name = forms.CharField(label='Your name', max_length=100)
    class Meta:
        model = DemoRequest
        fields = ('phone_number', 'name', 'email', 'region')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control', 'title': 'Ваш регион'}),
        }

        help_texts = {'region': None,}



    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        q = DemoRequest.objects.filter(phone_number=data)
        print(q)
        # Проверка на наличие заявок по данному номеру за последние 3 месяца
        if q:
            raise ValidationError('Данный номер телефона уже использовался ранее.')



        # Помните, что всегда надо возвращать "очищенные" данные.
        return data