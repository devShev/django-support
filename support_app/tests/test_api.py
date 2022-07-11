import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    client = APIClient()
    # Create user
    User.objects.create_user(username='user', password='simplepassword', email='user@example.com', is_staff=True)
    # Login by user
    get_token_url = reverse('token_obtain_pair')
    payload = {
        'username': 'user',
        'password': 'simplepassword',
    }
    response = client.post(get_token_url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    access_token = response.data.get('access')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client


@pytest.mark.django_db
def test_tickets(client):
    # Test POST method
    payload = {
        'subject': 'Test subject',
        'description': 'Test description',
    }
    response = client.post('/api/v1/tickets/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get('subject') == 'Test subject'
    assert response.data.get('description') == 'Test description'
    # Test GET method
    response = client.get('/api/v1/tickets/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0].get('subject') == 'Test subject'
    assert response.data[0].get('description') == 'Test description'
    # Test PUT method
    payload = {
        'subject': 'Test subject 2',
        'description': 'Test description 2',
        'status': 'frozen',
    }
    response = client.put('/api/v1/tickets/1/', payload, format='json')
    assert response.data.get('subject') == 'Test subject 2'
    assert response.data.get('description') == 'Test description 2'
    assert response.data.get('status') == 'frozen'
    # Test invalid status input (PUT method)
    payload = {
        'subject': 'Test subject',
        'description': 'Test description',
        'status': 'frozen1',
    }
    response = client.put('/api/v1/tickets/1/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
