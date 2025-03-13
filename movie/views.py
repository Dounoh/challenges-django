from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg,Count,Q
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .filter import FilmFilter
from .forms import CreateFilmForm
from .models import Film
from avis.forms import CritiqueForm
from account.models import User

class CreateFilmsView(LoginRequiredMixin,CreateView):
    
    model = Film
    form_class = CreateFilmForm
    template_name = 'movie/create_film.html'
    success_url = reverse_lazy('movie:film_view')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return redirect(self.success_url)
    
    
class FilmView(FilterView,ListView):
    model = Film
    template_name = 'movie/film_view.html'
    context_object_name = 'films'
    filterset_class = FilmFilter
    paginate_by = 8
    
    def get_queryset(self):
        queryset = Film.objects.filter(publie = True, accept_admin = True)
        value = self.request.GET.get('search')
        if value:
            queryset = queryset.filter(
                Q(title__icontains= value) | 
                Q(synopsis__icontains = value) | 
                Q(casting__icontains= value), 
                publie = True,
                accept_admin = True
                )
            return queryset
        else:
            return queryset
    

class DetailFilmView(DetailView):
    model = Film
    template_name = 'movie/detail_film.html'
    context_object_name = 'film'
    
    def get_object(self):
        uid = self.kwargs.get('uid')
        film = Film.objects.get(uid = uid)
        return film

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['critiques'] = context['film'].critiques.select_related('user').all()
        context['form'] = CritiqueForm
        return context 
    
class UpdateFilmView(LoginRequiredMixin,UpdateView):
    model = Film
    form_class = CreateFilmForm
    template_name = 'movie/update_film.html'
    success_url = reverse_lazy('movie:film_view')
    
    def get_object(self):
        uid = self.kwargs.get('uid')
        film = get_object_or_404(Film,uid=uid)
        return film

    
class DeleteFilmView(View):
    
    def get(self,request,uid):
        film = get_object_or_404(Film,uid=uid)
        film.delete()
        return redirect('movie:film_view')
    

