from __future__ import annotations

from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CommentaireViewSet
from .views import CritiqueViewSet
from .views import FilmDetailView
from .views import FilmListCreatView
from .views import InscriptionView


router = SimpleRouter()
router.register(r'critiques', CritiqueViewSet)
router.register(r'commentaires', CommentaireViewSet)

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('film-create-view/', FilmListCreatView.as_view(),
         name='film_create_view '),
    path('update-retrieve-destory/<int:pk>/', FilmDetailView.as_view(),
         name='film_update_retrieve_destory'),
] + router.urls
