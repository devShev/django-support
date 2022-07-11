from django.core.mail import send_mail

from support.celery import app


@app.task
def send_status_to_mail(status: str, email: str):

    if email:

        mail: int = send_mail(
            'Изменение статуса Тикета',
            f'Статус тикета обновился на - {status.capitalize()}',
            'devshevtestdrf@mail.ru',
            [email]
        )

        if mail:
            print(f'Mail send to {email}')
        else:
            print('The message has not been sent')
    else:
        print('Email not found!')
