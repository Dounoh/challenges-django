from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db import transaction
from django.views import View
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Survey, Question,Proposed
from .forms import SurveyForm, QuestionForm, ProposedFromSet



class SurveyDetailView(DetailView):
    template_name = 'sondage/detail_survey.html'
    context_object_name = 'survey'
    model = Survey
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionform'] = QuestionForm
        survey = self.get_object()
        question = Question.objects.filter(survey=survey)
        context['questions'] = question
        context['response_form'] = ProposedFromSet(queryset=Proposed.objects.none(), prefix='response')
        context['responses'] = None
        return context
    

class CreateSurveyView(CreateView):
    model = Survey
    form_class = SurveyForm
    context_object_name = 'form'
    template_name = "admin-survey/"

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.creator = self.request.user
        messages.success(self.request, 'sondage cree avec success')
        survey.save()
        return redirect('sondage:detail_survey', uid=survey.uid)


class CreateQuestion(CreateView):
    form_class = QuestionForm
    model = Question
    context_object_name = 'form'

    def form_valid(self, form):
        question = form.save(commit=False)
        uid = self.kwargs.get('uid') 
        survey = get_object_or_404(Survey, uid = uid)
        question.survey = survey
        question.save()
        return redirect('sondage:detail_survey', uid=uid)
    

class CreateProposedView(View):
    def post(self, request, uid,uid_question):
        form = ProposedFromSet(request.POST, prefix='response')
        if form.is_valid():
            question = get_object_or_404(Question, uid=uid)
            responses = form.save(commit=False)
            for response in responses:
                response.question = question
                response.save()
            messages.success(request,'Reponse ajouter avec success')
            return redirect('sondage:detail_survey', uid=uid_question)
        
        messages.error(request, 'le formulaire est invalide')
        return redirect('sondage:detail_survey', uid=uid_question)

