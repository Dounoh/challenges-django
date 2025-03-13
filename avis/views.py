from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import UpdateView,DetailView,DeleteView,CreateView,ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import LikeDislike
from .forms import CritiqueForm,CommentForm
from account.models import User
from .models import Critique,Commentaire
from movie.models import Film


@login_required
def like(request,uid):
    redirect_url = reverse_lazy('movie:film_view')
    film = Film.objects.get(uid=uid)
    
    post = LikeDislike.objects.filter(user = request.user, film =film).first()
    if post:
        if post.like:
            post.like = False
            post.save()
            messages.success(request,'le like supprimer avec success')
        else:
            post.like = True
            post.dislike = False
            post.save()
            messages.success(request,'le like a ete ajouter avec success')
        return redirect(redirect_url)
    else:
        LikeDislike.objects.create(user=request.user, film=film, dislike=False, like=True)
        messages.success(request,'le like ajouter avec success')
        return redirect(redirect_url)

@login_required       
def dislike(request,uid):
    redirect_url = reverse_lazy('movie:film_view')
    film = Film.objects.get(uid=uid)
    post = LikeDislike.objects.filter(user = request.user, film=film).first() 
    if post:
        if post.dislike:
            post.dislike= False
            post.save()
            messages.success(request,'le dislike supprimer avec success')
        else:
            post.dislike= True
            post.like = False
            post.save()
            messages.success(request,'le dislike a ete ajouter avec success')
        return redirect(redirect_url)
    else:
        LikeDislike.objects.create(user = request.user, film=film, like=False, dislike=True)
        messages.success(request,'le dislike ajouter avec success')
        return redirect(redirect_url)            


class CreateCritiqueView(LoginRequiredMixin,View):
    
    def post(self,request,uid):
        film = Film.objects.get(uid=uid)
        form = CritiqueForm(request.POST)
        if form.is_valid():
            if not Critique.objects.filter(user= request.user,film=film).exists():
                critique = form.save(commit=False)
                critique.user = request.user
                critique.film = film
                critique.save()
                return redirect('movie:film_detail',film.uid)
            else:
                messages.error(request,'Impossible d\'ajouter une nouvelle critique pour ce film')
                return redirect('movie:film_detail',film.uid)
        return redirect('movie:film_detail',film.uid)

class UpdateCritiqueView(LoginRequiredMixin,UpdateView):
    model = Critique
    form_class = CritiqueForm
    template_name = 'avis/update_critique.html'
    success_url = reverse_lazy('movie:')
    pk_url_kwarg = 'pk'
    
    def form_valid(self, form):
        critique = form.save(commit=False)
        critique.update_at = timezone.now()
        critique.save()
        return redirect('movie:')
    
class DeleteCritique(LoginRequiredMixin,View):
   def get(self,pk):
        try:
            critique = Critique.objects.get(pk=pk)
        except Critique.DoesNotExist:
            pass 
        critique.delete()
        return redirect('movie:')
    
class DetailCritiqueView(DetailView):
    model = Critique
    template_name = 'avis/comments.html'
    context_object_name = 'critique'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentaires'] = context['critique'].commentaires.select_related('user').all()
        print(context)
        context['form'] = CommentForm
        return context
    
    
class CreateCommentaireView(LoginRequiredMixin,CreateView):
    def post(self,request,pk):
        critique = Critique.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.critique = critique
            commentaire.user = request.user
            commentaire.save()
            messages.success(request,'Commentaire ajouter avec success')
            return redirect('avis:detail_critique',pk)
        
def deletecommante(request,comment,critique):
    commentaire = get_object_or_404(Commentaire,pk=comment)
    # critique = get_object_or_404(Critique,pk=critique)
    commentaire.delete()
    return redirect('avis:detail_critique',critique)

