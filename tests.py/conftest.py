from __future__ import annotations

from datetime import date

import pytest
from django.utils import timezone
from django.utils.timezone import timedelta
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from avis.models import Commentaire
from avis.models import Critique
from avis.models import LikeDislike
from movie.models import Film


@pytest.fixture
def user_create():
    user = User.objects.create_user(
        first_name='test_first',
        last_name='test_last',
        email='test@gmail.com',
        role='realisateur',
        password='12345'
    )
    return user


@pytest.fixture
def create_film(user_create):
    return Film.objects.create(
        user=user_create,
        title='film 1',
        synopsis='le film test',
        genre='action',
        out_date=date(2024, 5, 20),
        casting='',
        duree='',
    )


@pytest.fixture
def create_critique(user_create, create_film):
    return Critique.objects.create(
        film=create_film,
        user=user_create,
        title='commentaire 1',
        description='description',
        note=3,

    )


@pytest.fixture
def create_commentaire(user_create, create_critique):
    return Commentaire.objects.create(
        critique=create_critique,
        user=user_create,
        comment='super'
    )


@pytest.fixture
def create_likedislike(user_create, create_film):
    like = [LikeDislike.objects.create(
        user=user_create, film=create_film, like=True) for _ in range(10)]
    dislike = [LikeDislike.objects.create(
        user=user_create, film=create_film, dislike=True) for _ in range(4)]
    return like, dislike


@pytest.fixture
def data_serializer():
    data = {
        'first_name': 'test_first',
        'last_name': 'test_last',
        'email': 'test@gmail.com',
        'role': 'realisateur',
        'password1': 'Guinee224',
        'password2': 'Guinee224'
    }
    return data


@pytest.fixture
def api_client(APIClient):
    return APIClient


@pytest.fixture
def user_auth(user_create, api_client):
    user = user_create
    user.is_active = True
    user.save()

    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
    return api_client, user
