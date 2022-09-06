from django.core.mail import send_mail
import requests


def send_to_email(email, payload):

    send_mail(
        payload['fields']['TITLE'],
        payload,
        'pass.artyom@gmail.com',
        [email],
        fail_silently=False,
    )


payload = {
                    "fields":
                        {
                            "TITLE": "Заявка по демодоступу ("")",
                            "NAME": 'Artem',
                            "STATUS_ID": "NEW",
                            "OPENED": "Y",
                            "ASSIGNED_BY_ID": 1,
                            "COMMENTS": "Регион: ",
                            "PHONE": '89823105691'
                        }}


send_to_email('artyom.pass@yandex.ru', payload)
