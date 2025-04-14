from django.shortcuts import render, redirect,HttpResponse
from django.views.generic import CreateView, DetailView, TemplateView
from django.views import View

from sondage.forms import SurveyForm

from sondage.models import Survey

def index(request):
    return render(request, 'admin-survey/dashboard.html')

class DashboardView(TemplateView):
    template_name = 'admin-survey/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SurveyForm
        context['surveys'] = Survey.objects.filter(creator = self.request.user)
        return context
    