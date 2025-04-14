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

def index(request):
    return render(request,'sondage/index.html')


class SurveyDetailView(DetailView):
    template_name = 'sondage/add_question.html'
    context_object_name = 'survey'
    model = Survey
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionform'] = QuestionForm
        survey = self.get_object()
        context['questions'] = Question.objects.filter(survey=survey)
        context['response_form'] = ProposedFromSet(queryset=Proposed.objects.none(), prefix='response')
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
    template_name = ''
    context_object_name = 'form'

    def form_valid(self, form):
        question = form.save(commit=False)
        uid = self.kwargs.get('uid') 
        survey = get_object_or_404(Survey, uid = uid)
        question.survey = survey
        question.save()
        return redirect('sondage:detail_survey', uid=uid)
    
# class CreateProposedView(CreateView):
#     form_class = ProposedFromSet
#     model = Proposed
#     template_name = ''

#     def form_valid(self, form):
#         proposed = form.save(commit=False)
#         uid = self.kwargs.get('uid')
#         question = get_object_or_404(Question, uid=uid)
#         proposed.question = question
#         proposed.save()
#         return redirect('sondage:detail_survey', uid=uid)
    

class CreateProposedView(View):
    def get(self, request, uid):
        formset = ProposedFromSet(queryset=Proposed.objects.none())
        return render(request, 'sondage/proposed_form.html', {
            'formset': formset,
            'uid': uid,
        })

    def post(self, request, uid):
        formset = ProposedFromSet(request.POST)
        if formset.is_valid():
            question = get_object_or_404(Question, uid=uid)
            for form in formset:
                if form.cleaned_data:  # pour éviter les lignes vides
                    proposed = form.save(commit=False)
                    proposed.question = question
                    proposed.save()
            return redirect('sondage:detail_survey', uid=uid)
        # Si le formulaire n’est pas valide, on le réaffiche
        return HttpResponse('le formulaire invalide')