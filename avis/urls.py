from django.urls import path
from .views import like,dislike,CreateCritiqueView,UpdateCritiqueView
from .views import DeleteCritique,DetailCritiqueView,CreateCommentaireView
from .views import deletecommante

app_name = 'avis'
urlpatterns = [
    
    path('add-like-film/<str:uid>/',like,name='like'),
    path('dislike-film/<str:uid>/',dislike,name='dislike'),
    path('Critique-film/<str:uid>/',CreateCritiqueView.as_view(),name='critique'),
    path('Update-critique/<int:pk>/',UpdateCritiqueView.as_view(),name='critique_update'),
    path('Delete-critique/<int:pk>/',DeleteCritique.as_view(),name='delete_critique'),
    path('Detail-critique/<int:pk>/',DetailCritiqueView.as_view(),name='detail_critique'),
    path('commentaire/<int:pk>/',CreateCommentaireView.as_view(),name='commentaire'),
    path('Delete-commentaire/<int:comment>/<int:critique>/',deletecommante,name='delete_commentaire'),
    
]
