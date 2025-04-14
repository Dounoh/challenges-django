from django.urls import path
from .views import index,CreateSurveyView,SurveyDetailView, CreateQuestion,CreateProposedView

app_name = 'sondage'
urlpatterns = [
    path('',index,name='index'),
    path('create-survey/',CreateSurveyView.as_view(), name='create_survey'),
    path('detail-survey/<str:uid>',SurveyDetailView.as_view(), name='detail_survey'),

    path('create-question/<str:uid>/',CreateQuestion.as_view(), name='create_question'),

    path('create-response/<str:uid>/',CreateProposedView.as_view(), name='create_response')
]
