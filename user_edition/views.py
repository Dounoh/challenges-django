from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View

from movie.models import Film
from movie.forms import CreateFilmForm

class FilmUserView(ListView):
    template_name = 'user_edition/film_user.html'
    model = Film
    context_object_name = 'user_films'
    
    def get_queryset(self):
        queryset = Film.objects.filter(user = self.request.user, publie = True)
        return queryset
    
class BrouillonUserView(ListView):
    template_name = 'user_edition/user_brouillons.html'
    model = Film
    context_object_name = 'user_films'
    
    def get_queryset(self):
        queryset = Film.objects.filter(user = self.request.user, publie = False)
        return queryset

class UpdateUserFilmView(LoginRequiredMixin,UpdateView):
    model = Film
    form_class = CreateFilmForm
    template_name = 'user_edition/user_edit.html'
    success_url = reverse_lazy('user_edition:user_brouillon')
    
    def get_object(self):
        uid = self.kwargs.get('uid')
        film = get_object_or_404(Film,uid=uid)
        return film


class DeleteUserFilmView(View):
    
    def get(self,request,uid):
        film = get_object_or_404(Film,uid=uid)
        if request.user == film.user:
            film.delete()
            return redirect('user_edition:user_brouillon')
        else:
            return redirect('movie:film_view')
