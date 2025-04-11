from django.shortcuts import render, redirect,HttpResponse
from django.forms import inlineformset_factory
from django.db import transaction
from django.views import View
from django.urls import reverse_lazy

from .forms import SurveyForm, QuestionForm, ChoiceFormSet
from sondage.models import Question, Choice, Survey

def index(request):
    return render(request, 'admin-survey/dashboard.html')

def index1(request):
    return render(request, 'admin-survey/add_survey.html')

class CreateSurveyView(View):
    redirect_url = reverse_lazy('admin-survey:dashbord')

    def get(self, request):
        surveyform = SurveyForm()
        questionform = QuestionForm()
        choiceform = ChoiceFormSet(queryset=Choice.objects.none() , prefix='choise_from')
        context = {
            'surveyform': surveyform,
            'questionform': questionform,
            'choiceform': choiceform,
        }
        return render(request, 'admin-survey/add_survey.html', context)
    
    def post(self, request):
        surverform = SurveyForm(request.POST)
        questionform = QuestionForm(request.POST)
        choiceform = ChoiceFormSet(request.POST)

        if surverform.is_valid() and questionform.is_valid() and choiceform.is_valid():
            with transaction.atomic():
                survey = surverform.save(commit=False)
                survey.creator = request.user
                survey.save()

                question = questionform.save(commit=False)
                question.survey = survey
                q = question.save()

                for choise in choiceform:
                    choise.question = q
                    choise.save()
            return HttpResponse('success')

