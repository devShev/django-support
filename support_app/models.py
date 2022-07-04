from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Ticket(models.Model):
    """Тикет"""

    class TicketStatus(models.TextChoices):
        active = 'AC', _('Активно')
        solved = 'SO', _('Решено')
        unsolved = 'UN', _('Не решено')
        frozen = 'FR', _('Заморожено')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    subject = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=300,
    )

    status = models.CharField(
        max_length=2,
        choices=TicketStatus.choices,
        default=TicketStatus.active,
    )

    created_date = models.DateTimeField(
        default=timezone.now,
    )


class Message(models.Model):
    """Сообщение"""

    ticket = models.ForeignKey(
        Ticket,
        verbose_name='Тикет',
        on_delete=models.CASCADE,
        null=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    message = models.TextField(
        max_length=300,
        verbose_name='Сообщене',
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата сообщения',
        default=timezone.now,
    )

    is_read = models.BooleanField(
        verbose_name='Прочитано',
        default=False,
    )







