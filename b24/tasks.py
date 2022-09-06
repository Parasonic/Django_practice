from django.core.mail import send_mail
import requests
from celery import shared_task


# Отдельные функции передачи заявок во внешние сервисы,
# запускается в отдельных потоках Celery
@shared_task()
def send_to_email(email, subject, message):

    send_mail(
        subject,
        message,
        'pass.artyom@gmail.com',
        [email],
        fail_silently=False,
    )


@shared_task()
def send_to_b24(webhook, payload):
    r = requests.post(webhook+'crm.lead.add', json=payload)
    print(r.text)


@shared_task()
def test_task(payload):
    print(payload)