from django.db import models
from django.db.models import Avg,F,Count
import uuid

GENRES = [
        ('action', 'Action'),
        ('drama', 'Drama'),
        ('comedy', 'Comedy'),
    ]

class Film(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey('account.User',on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=30,blank=False,null=False)
    synopsis = models.TextField()
    genre = models.CharField(max_length=20,choices=GENRES)
    out_date = models.DateField()
    casting = models.CharField(max_length=250)
    duree = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media/film',blank=False,null=True)
    publie = models.BooleanField(default=False)
    accept_admin = models.BooleanField(default=False)
    
    @property
    def note_moyenne(self):
        moyenne = self.critiques.aggregate(moyenne = Avg('note'))['moyenne']
        return moyenne if moyenne is not None else 0.0
    
    @property
    def like_count(self):
        likes = self.like_film.filter(like = True).count()
        return likes if likes is not None else 0
    
    @property
    def dislike_count(self):
        dislikes = self.like_film.filter(dislike = True).count()
        return dislikes if dislikes is not None else 0