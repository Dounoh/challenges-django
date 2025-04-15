from django.urls import path
from .views import ListeSurveyView, DetailSurvey

app_name = 'participant'
urlpatterns = [
    path('', ListeSurveyView.as_view(), name='liste_survey'),
    path('detail-survey/<str:uid>/', DetailSurvey.as_view(), name='detail_survey')
]
