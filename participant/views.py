from django.shortcuts import render
from django.views.generic import ListView,DetailView

from sondage.models import Question,Survey

class ListeSurveyView(ListView):
    model = Question
    template_name = 'participant/index.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        quesryset = Survey.objects.select_related('creator').all()
        return quesryset
    

class DetailSurvey(DetailView):
    model = Survey
    template_name = 'participant/response_survey.html'
    context_object_name = 'survey'
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    