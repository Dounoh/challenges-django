from __future__ import annotations

import pytest
from django.test import client
from django.urls import reverse
from django.urls import reverse_lazy

from account.forms import ForgotPasswordForm
from account.models import User


@pytest.mark.django_db
def test_login_view(client):
    url = reverse('account:login')
    user = User.objects.create_user(
        first_name='test_first',
        last_name='test_last',
        email='test@gmail.com',
        role='realisateur',
        password='12345',
        is_active=True
    )

    data = {
        'username': 'test@gmail.com',
        'password': '12345'
    }
    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse('movie:film_view')


@pytest.mark.django_db
def test_creation_account(client):
    url = reverse_lazy('account:register')
    data = {
        'first_name': 'test_first',
        'last_name': 'test_last',
        'email': 'test1@gmail.com',
        'role': 'realisateur',
        'password1': 'Guinee224',
        'password2': 'Guinee224'
    }
    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse('account:login')
    assert User.objects.filter(email='test1@gmail.com').exists()


@pytest.mark.django_db
def test_forgot_password(client, user_create):
    url = reverse('account:forgot_password')
    data = {
        'email': 'test@gmail.com'
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('account:login')


@pytest.mark.django_db
def test_forgot_password_false(client, user_create):
    url = reverse('account:forgot_password')
    data = {
        'email': 'teee@gmail.com'
    }
    response = client.post(url, data=data)

    assert response.status_code == 200
    form = ForgotPasswordForm(data=data)
    assert not form.is_valid()
    assert "Erreur aucun compte associer à ce mail" in form.errors["email"]
