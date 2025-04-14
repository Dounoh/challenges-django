from django.db import models
from django.utils import timezone
import uuid


#Titre, description, date de début, date de fin, créateur (FK vers User).
class Survey(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title_survey = models.CharField(max_length=100, verbose_name='Titre')
    description = models.TextField(max_length=400, verbose_name='Description')
    start_date = models.DateField(blank=False, null=False, verbose_name='Debut')
    end_date = models.DateField(blank=False, null=False, verbose_name='Fin')
    create_at = models.DateField(auto_now_add=True)
    creator = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='creator')

    def __str__(self):
        return self.title


#Texte de la question, type de réponse (réponse unique, multiple ou texte), sondage (FK vers Survey)
class Question(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name='questions')
    title_question = models.CharField(max_length=200, verbose_name='Titre')
    choice = models.ForeignKey('Choice', on_delete=models.PROTECT)

    def __str__(self):
        return self.title_question


# Option de réponse pour les questions de type choix, question (FK vers Question).
class Choice(models.Model):  
    choice = models.CharField(max_length=200, verbose_name='choix',null=True)  
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.choice


class Proposed(models.Model):
    uid = models.URLField(default=uuid.uuid4, unique=True, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.CharField(max_length=200, null=False, blank=False)
    create_at = models.DateField(auto_now_add=True)


# Lien entre la question et la réponse donnée par un utilisateur, avec FK vers User et vers Survey.
class Response(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='responses')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response de {self.user} a {self.question}"

#Réponse du participant à la question (soit choix, soit texte)
# class Answers(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='user')
#     question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question_answer')
#     survey = models.ForeignKey(Survey,on_delete=models.CASCADE)
#     avis_unique = 
#     create_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('question','user')
    
#     def __str__(self):
#         return f'{self.question.title} - {self.user.first_name}'