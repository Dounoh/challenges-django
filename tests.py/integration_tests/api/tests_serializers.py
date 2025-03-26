from __future__ import annotations

import pytest

from account.models import User
from api.serializers import InscriptionUserSerializer


@pytest.mark.django_db
def test_inscription_serializer_error(data_serializer):
    data = data_serializer
    data['password1'] = '12345'
    data['password2'] = '12345ZEX'

    serializer = InscriptionUserSerializer(data=data)
    assert not serializer.is_valid()
    assert "les mots de passes sont different" in serializer.errors


@pytest.mark.django_db
def test_inscription_serializer_error(data_serializer):
    data = data_serializer
    serializer = InscriptionUserSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_save_serializer(data_serializer):
    data = data_serializer
    serializer = InscriptionUserSerializer(data=data)
    assert serializer.is_valid()
    serializer.save()
    assert User.objects.filter(email='test@gmail.com').exists()
