from __future__ import annotations

from django.urls import path

from .views import CreateFilmsView
from .views import DeleteFilmView
from .views import DetailFilmView
from .views import FilmView
from .views import UpdateFilmView

app_name = 'movie'
urlpatterns = [
    path('create-film/', CreateFilmsView.as_view(), name='create_film'),
    path('', FilmView.as_view(), name='film_view'),
    path('film-datail/<str:uid>', DetailFilmView.as_view(), name='film_detail'),
    path('Update-film/<str:uid>/', UpdateFilmView.as_view(), name='update_film'),
    path('Delete-film/<str:uid>', DeleteFilmView.as_view(), name='delete_film'),

]
