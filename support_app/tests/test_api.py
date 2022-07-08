import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_create_user():
    # Create user
    payload = {
      "email": "user@example.com",
      "username": "user",
      "password": "simplepassword",
    }
    response = client.post('/auth/users/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_bad_create_user():
    # Bad create user
    payload = {
      "email": "user@example.com",
      "username": "user",
      "password": "1234",
    }
    response = client.post('/auth/users/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_tickets():
    # Create user
    payload = {
      "email": "user@example.com",
      "username": "user",
      "password": "simplepassword",
    }
    response = client.post('/auth/users/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

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

    # Test POST method
    payload = {
        'subject': 'Test subject',
        'description': 'Test description',
    }
    response = client.post('/api/v1/tickets/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Test GET method
    response = client.get('/api/v1/tickets/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0].get('subject') == 'Test subject'
    assert response.data[0].get('description') == 'Test description'
