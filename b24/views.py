from django.shortcuts import render
from .models import Partner, Region, DemoRequest
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import DemoForm, VerificationForm
import random, requests, time, aiohttp
from django.core.mail import send_mail
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import threading
from django.contrib import messages
from .tasks import test_task, send_to_b24, send_to_email
# from .smsc_api import *


def thread_send_to_email(webhook, payload):
    r = requests.post(webhook+'crm.lead.add', json=payload)
    print(r.text)
    print('Поток завершён')


# Отдельная функция передачи заявок во внешние сервисы, запускается в отдельном потоке,
# чтобы не блокировать основной
def thread_send_to(email, webhook, payload):
    send_mail(
        'Новая заявка',
        'Тестовый текст',
        'pass.artyom@gmail.com',
        [email],
        fail_silently=False,
    )

    if webhook:
        print(webhook)
        r = requests.post(webhook+'crm.lead.add', json=payload)
        print(r.text)


def index(request):
    # Пересчёт записей основных объектов в БД (информация выводится в шаблоне)
    num_partner = Partner.objects.all().count()
    num_region = Region.objects.all().count()
    num_demo_requests = DemoRequest.objects.count()

    context = {
        'num_partner': num_partner,
        'num_region': num_region,
        'num_demo_requests': num_demo_requests,
    }

    # Если запрос типа POST - обрабатываем данные из формы
    if request.method == 'POST':

        # Создаём экземпляр формы и наполняем данными из запроса:
        form1 = DemoForm(request.POST)

        # Блок срабатывающий если форма прошла валидацию:
        if form1.is_valid():

            # Пробуем найти по указанному номеру телефона неподтверждённую ранее заявку.
            # Если находим, обновляем её и перенаправляем на страницу валидации.
            try:
                demo_request = DemoRequest.objects.get(phone_number__exact=form1.cleaned_data['phone_number'])
                form1 = DemoForm(request.POST, instance=demo_request)
                chosen_partner = random.choice(Partner.objects.filter(region__exact=form1['region'].value()))
                f = form1.save()
                f.partner = chosen_partner
                f.save()
                request.session['phone_number'] = form1['phone_number'].value()
                return redirect('token_validation/')

            # Если не находим, сохраняем Заявку, добавив случайно выбранного партнёра в поле partner.
            except ObjectDoesNotExist:
                form1 = DemoForm(request.POST)
                chosen_partner = random.choice(Partner.objects.filter(region__exact=form1['region'].value()))
                f = form1.save()
                f.partner = chosen_partner
                f.save()
                request.session['phone_number'] = form1['phone_number'].value()
                return redirect('token_validation/')

    # Если запрос типа GET - создаём пустую форму для передачи в рендер
    else:
        form1 = DemoForm()

    context = {
        'num_partner': num_partner,
        'num_region': num_region,
        'num_demo_requests': num_demo_requests,
        'form': form1,
    }

    # payload = {
    #     "fields":
    #         {
    #             "TITLE": "Заявка по демодоступу ("")",
    #             "NAME": 'Artem',
    #             "STATUS_ID": "NEW",
    #             "OPENED": "Y",
    #             "ASSIGNED_BY_ID": 1,
    #             "COMMENTS": "Регион: ",
    #             "PHONE": '89823105691'
    #         }}
    #
    # print('test')
    #
    # email = 'artyom.pass@yandex.ru'
    #
    # send_mail(
    #         "Заявка по демодоступу ("")",
    #         'Тестовый текст',
    #         'pass.artyom@gmail.com',
    #         [email],
    #         fail_silently=False,
    #     )

    # Рендер шаблона index.html с данными переменной context
    return render(request, 'index.html', context=context)



            # # Сохраняем Заявку, добавив случайно выбранного партнёра в поле partner
            # # chosen_partner = random.choice(Partner.objects.filter(region__exact=form1['region'].value()))
            # # f = form1.save(commit=False)
            # # f.partner = chosen_partner
            # # f.save()
            #
            # # Запускаем функцию рассылки в отдельном потоке
            # x = threading.Thread(target=thread_send_to, args=(chosen_partner.email, chosen_partner.webhook, payload), daemon=False)
            # x.start()
            # # smsc = SMSC()
            # # r = smsc.send_sms("79823105691", "Ваш пароль: 123", sender="sms")
            # r = requests.post("https://sms.ru/sms/send?api_id=B53FA6D1-EF23-B17F-BBD6-9D5BD11C4729&to=" + "79823105691"
            #                   + "&msg=" + "hello+world" + "&json=1", json=payload)
            #
            #
            # # Обновляем информацию о количестве заявок и возвращаем пользователю страницу с благодарностями
            # num_demo_requests = DemoRequest.objects.count()
            # context['num_demo_requests'] = num_demo_requests
            # request.session['phone_number'] = form1['phone_number'].value()
            # # request.session['_prev_form'] = form1
            # # form = VerificationForm()
            # # context['form'] = form
            # return redirect('token_validation/')

    # Если запрос типа GET - создаём пустую форму для передачи в рендер
    # else:
    #     form1 = DemoForm()
    #
    # context = {
    #     'num_partner': num_partner,
    #     'num_region': num_region,
    #     'num_demo_requests': num_demo_requests,
    #     'form': form1,
    # }
    #
    # # Рендер шаблона index.html с данными переменной context
    # return render(request, 'index.html', context=context)


def token_validation(request):
    demo_request = DemoRequest.objects.get(phone_number__exact=request.session['phone_number'])

    context = {
        'request_phone': demo_request.phone_number,
        'request_name': demo_request.name,
        'request_region': demo_request.region,
    }

    form2 = VerificationForm(request.POST)
    context['form'] = form2

    if request.method == 'POST':

        # form = VerificationForm(request.POST)
        demo_request = DemoRequest.objects.get(phone_number__exact=request.session['phone_number'])

        if form2.is_valid():
            if form2.cleaned_data['verification_code'] == demo_request.verification_code:
                demo_request.is_verified = True
                demo_request.save()

                payload = {
                    "fields":
                        {
                            "TITLE": "Заявка по демодоступу (" + demo_request.name + ")",
                            "NAME": demo_request.name,
                            "STATUS_ID": "NEW",
                            "OPENED": "Y",
                            "ASSIGNED_BY_ID": 1,
                            "COMMENTS": "Регион: " + str(demo_request.region),
                            "PHONE": [{"VALUE": demo_request.phone_number, "VALUE_TYPE": "WORK"}]
                        }}

                # chosen_partner = random.choice(Partner.objects.filter(region__exact=demo_request.region))

                send_to_b24.delay(demo_request.partner.webhook, payload)
                send_to_email.delay(demo_request.partner.email, str(payload['fields']['TITLE']), str(payload))

                return redirect('thanks')

            else:
                messages.error(request, 'Неверный код, попробуйте ещё раз.')

    return render(request, 'token_validation.html', context=context)


def thanks(request):
    num_partner = Partner.objects.all().count()
    num_region = Region.objects.all().count()
    num_demo_requests = DemoRequest.objects.count()

    context = {
        'num_partner': num_partner,
        'num_region': num_region,
        'num_demo_requests': num_demo_requests,
    }

    return render(request, 'thanks.html', context=context)

# payload = {
#     "fields":
#         {
#             "TITLE": "Заявка по демодоступу ("+form1['name'].value()+")",
#             "NAME": form1['name'].value(),
#             "STATUS_ID": "NEW",
#             "OPENED": "Y",
#             "ASSIGNED_BY_ID": 1,
#             "COMMENTS": "Регион: "+form1['region'].value(),
#             "PHONE": [{"VALUE": form1['phone_number'].value(), "VALUE_TYPE": "WORK"}]
#         }}