from __future__ import annotations

import pytest

from movie.models import Film


@pytest.mark.django_db
def test_add_film(create_film):
    film = create_film
    assert Film.objects.count() == 1
    assert film.title == 'film 1'
    assert film.publie == False
