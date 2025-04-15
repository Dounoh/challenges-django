from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from sondage.models import Question,Survey,Proposed
from django.views import View 

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        question = survey.questions.all()
        context['questions'] = question
        return context
    
def get_question(request,uid):
    question = get_object_or_404(Question, uid=uid)
    pass

class AnswerQuestionView(View):
    def post(resquest,uid,type):
        question = question(resquest, uid)
        if 'unique' == type:
            pass
