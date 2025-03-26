from __future__ import annotations

from django.urls import path

from .views import BrouillonUserView
from .views import DeleteUserFilmView
from .views import FilmUserView
from .views import UpdateUserFilmView

app_name = 'user_edition'
urlpatterns = [
    path('user-film/', FilmUserView.as_view(), name='user_film'),
    path('user-brouillons/', BrouillonUserView.as_view(), name='user_brouillon'),
    path('user-update-film/<str:uid>',
         UpdateUserFilmView.as_view(), name='update_user_film'),
    path('user-film/<str:uid>/', DeleteUserFilmView.as_view(),
         name='user_delete_film'),

]
