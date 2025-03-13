from django.urls import path
from .views import CreateFilmsView,FilmView,DetailFilmView,UpdateFilmView
from .views import DeleteFilmView

app_name = 'movie'
urlpatterns = [
    path('create-film/',CreateFilmsView.as_view(),name='create_film'),
    path('',FilmView.as_view(),name='film_view'),
    path('film-datail/<str:uid>',DetailFilmView.as_view(),name='film_detail'),
    path('Update-film/<str:uid>/',UpdateFilmView.as_view(),name='update_film'),
    path('Delete-film/<str:uid>',DeleteFilmView.as_view(),name='delete_film'),
    
]
