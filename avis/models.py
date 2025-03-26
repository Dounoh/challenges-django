from __future__ import annotations

from django.db import models
from django.utils import timezone

from account.models import User


note_choix = [
    (1, 'movais'),
    (2, 'passable'),
    (3, 'A bien'),
    (4, 'Bien'),
    (5, 'Exelent')
]


class Critique(models.Model):
    film = models.ForeignKey(
        'movie.Film', on_delete=models.CASCADE, related_name='critiques')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='critiques_user')
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=250, null=False, blank=False)
    note = models.PositiveBigIntegerField(choices=note_choix, default=1)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'title {self.film}'


class Commentaire(models.Model):
    critique = models.ForeignKey(
        Critique, on_delete=models.CASCADE, related_name='commentaires')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commentaires_user')
    comment = models.TextField(max_length=100)
    at_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'commentaire {self.user.first_name}'


class LikeDislike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='like_user')
    film = models.ForeignKey(
        'movie.Film', on_delete=models.CASCADE, related_name='like_film')
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ('user','like','dislike')
