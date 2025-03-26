from __future__ import annotations

import pytest
from django.test import client

from account.models import User


@pytest.mark.django_db
def test_user_crate_account(user_create):
    user = user_create
    assert User.objects.count() == 1
    assert user.first_name == 'test_first'
    assert user.is_active == False


@pytest.mark.django_db
def test_check_login_no_activate_account(client, user_create):
    user = user_create
    response = client.login(email='test@gmail.com', password="12345")
    assert response is False
