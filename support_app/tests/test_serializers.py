import pytest
from django.contrib.auth.models import User

from support_app.models import Message, Ticket
from support_app.serializers import MessageSerializer, TicketSerializer


@pytest.mark.django_db
def test_ticket_serializer():
    user = User.objects.create()

    ticket = Ticket.objects.create(
        author=user,
        subject='Test subject',
        description='Test description',
    )

    serializer_data = TicketSerializer(ticket).data

    assert serializer_data.get('id') == ticket.id
    assert serializer_data.get('author_id') == user.id
    assert serializer_data.get('subject') == 'Test subject'
    assert serializer_data.get('description') == 'Test description'
    assert serializer_data.get('status') == 'active'


@pytest.mark.django_db
def test_message_serializer():
    user = User.objects.create()
    ticket = Ticket.objects.create(
        author=user,
        subject='Test subject',
        description='Test description',
    )

    message = Message.objects.create(
        ticket=ticket,
        author=user,
        message='Test message',
    )

    serializer_data = MessageSerializer(message).data

    assert serializer_data.get('id') == message.id
    assert serializer_data.get('ticket_id') == ticket.id
    assert serializer_data.get('author_id') == user.id
    assert serializer_data.get('message') == 'Test message'
