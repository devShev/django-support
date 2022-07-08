from support.celery import app
from django.core.mail import send_mail
from .models import Ticket


@app.task
def send_status_to_mail(ticket: Ticket):

    email = ticket.author.email

    if email:
        status = ticket.status

        mail = send_mail(
            'Изменение статуса Тикета',
            f'Статус тикета обновился на - {status}',
            'devshevtestdrf@mail.ru',
            [email]
        )

        if mail:
            print('The message has been sent')
        else:
            print('The message has not been sent')
    else:
        print('Email not found!')
