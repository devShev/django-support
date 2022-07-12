import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from support_app.models import Ticket


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='user',
        password='simplepassword',
        email='user@example.com', is_staff=True
    )

    return user


@pytest.fixture
def client(user):
    client = APIClient()
    # Login by user
    get_token_url = reverse('token_obtain_pair')
    payload = {
        'username': 'user',
        'password': 'simplepassword',
    }
    response = client.post(get_token_url, payload, format='json')
    access_token = response.data.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    return client


@pytest.fixture
def ticket(user):
    ticket = Ticket.objects.create(
        author=user,
        subject='Test ticket',
        description='Test description'
    )

    return ticket
