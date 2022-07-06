from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TicketStatus(models.TextChoices):
    active = 'active', _('active')
    solved = 'solved', _('solved')
    unsolved = 'unsolved', _('unsolved')
    frozen = 'frozen', _('frozen')


class Ticket(models.Model):
    """Ticket"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author",
    )

    subject = models.CharField(
        max_length=100,
        verbose_name='Subject',
    )

    description = models.TextField(
        max_length=500,
        verbose_name='Description',
    )

    status = models.CharField(
        max_length=10,
        choices=TicketStatus.choices,
        default=TicketStatus.active,
        verbose_name='Status',
    )

    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created date',
    )

    def __str__(self):
        return str(self.subject) + " - " + str(self.status)


class Message(models.Model):
    """Message"""

    ticket = models.ForeignKey(
        Ticket,
        verbose_name='Ticket',
        on_delete=models.CASCADE,
        null=True,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author of message',
    )

    message = models.TextField(
        max_length=500,
        verbose_name='Message text',
    )

    pub_date = models.DateTimeField(
        verbose_name='Message date',
        default=timezone.now,
    )
