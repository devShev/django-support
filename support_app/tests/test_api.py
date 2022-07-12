import pytest
from rest_framework import status

from ..serializers import TicketSerializer
from .fixtures import client, ticket, user


@pytest.mark.django_db
def test_post_ticket(client, user):
    # Test POST method
    payload = {
        'subject': 'Test subject',
        'description': 'Test description',
    }
    response = client.post('/api/v1/tickets/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    expected_data = {
        'id': response.data.get('id'),
        'author_id': user.id,
        'subject': payload.get('subject'),
        'description': payload.get('description'),
        'created_date': response.data.get('created_date'),
        'status': 'active',
    }
    assert response.data == expected_data


@pytest.mark.django_db
def test_get_ticket(client, ticket):
    response = client.get('/api/v1/tickets/')
    assert response.status_code == status.HTTP_200_OK

    expected_data = TicketSerializer(ticket).data
    assert response.data[0] == expected_data


@pytest.mark.django_db
def test_put_ticket(client, ticket, user):
    payload = {
        'subject': 'Test subject 2',
        'description': 'Test description 2',
        'status': 'frozen',
    }
    response = client.put(f'/api/v1/tickets/{ticket.pk}/', payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    expected_data = {
        'id': ticket.pk,
        'author_id': user.pk,
        'subject': payload.get('subject'),
        'description': payload.get('description'),
        'created_date': TicketSerializer(ticket).data.get('created_date'),
        'status': payload.get('status'),
    }
    assert response.data == expected_data


@pytest.mark.django_db
def test_bad_put_ticket(client, ticket):
    payload = {
        'subject': 'Test subject',
        'description': 'Test description',
        'status': 'frozen1',
    }
    response = client.put(f'/api/v1/tickets/{ticket.pk}/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_message(client, ticket, user):
    payload = {
        'message': 'Test message'
    }
    response = client.post(f'/api/v1/tickets/{ticket.id}/msg/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    expected_data = {
        'id': response.data.get('id'),
        'ticket_id': ticket.pk,
        'author_id': user.pk,
        'message': payload.get('message'),
        'pub_date': response.data.get('pub_date'),
    }
    assert response.data == expected_data
