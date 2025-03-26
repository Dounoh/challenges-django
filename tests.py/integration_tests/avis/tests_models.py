from __future__ import annotations

import pytest

from account.models import User
from avis.models import Commentaire
from avis.models import Critique
from avis.models import LikeDislike
from movie.models import Film


@pytest.mark.django_db
def test_critique(create_critique, user_create):
    critique = create_critique
    assert Critique.objects.count() == 1
    assert critique.title == 'commentaire 1'
    assert critique.user == user_create
    assert critique.note == 3


@pytest.mark.django_db
def test_commentaire(create_critique, user_create, create_commentaire):
    user = User.objects.create_user(
        first_name='first_comment',
        last_name='last_comment',
        email='comment@gmail.com',
        role='utilisateur',
        password='12345'
    )

    comment = Commentaire.objects.create(
        critique=create_critique,
        user=user,
        comment='trop bon'
    )

    assert Commentaire.objects.count() == 2
    assert comment.user == user


@pytest.mark.django_db
def test_like_dislike(create_likedislike):
    like, dislike = create_likedislike
    film = like[0].film
    assert film.like_count == 10
    assert film.dislike_count == 4
