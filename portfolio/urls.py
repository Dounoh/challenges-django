from django.urls import path
from .views import ViewPortfolio

urlpatterns = [
    path('',ViewPortfolio.as_view(),name='accueil'),
]