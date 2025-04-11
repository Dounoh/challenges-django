from django.db import models
from django.utils import timezone
import uuid

class Survey(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title_survey = models.CharField(max_length=100, verbose_name='Titre')
    description = models.TextField(max_length=400, verbose_name='Description')
    start_date = models.DateField(default=timezone.now, verbose_name='Debut')
    end_date = models.DateField(default=timezone.now, verbose_name='Fin')
    create_at = models.DateField(auto_now_add=True)
    creator = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='creator')

    def __str__(self):
        return self.title


class Question(models.Model):
    CHOISE_QUESTION = [
        ('unique','Réponse unique'),
        ('multiple','Réponse multiple'),
        ('ouverte','Réponse texte ouverte')
    ]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    survey = models.ForeignKey(Survey,on_delete=models.PROTECT,related_name='questions')
    title_question = models.CharField(max_length=200, verbose_name='Titre')
    type_answer = models.CharField(max_length=21,choices=CHOISE_QUESTION ,default='unique')

    def __str__(self):
        return self.title


class Choice(models.Model):  
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='choices')
    answer_text = models.CharField(max_length=200,verbose_name='Reponse',null=True)  
    is_correct = models.BooleanField(default=False)  

    def __str__(self):
        return self.answer_text


class Response(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='responses')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response de {self.user} a {self.question}"


class Answers(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='user')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question_answer')
    choix = models.ForeignKey(Choice,on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question','user')
    
    def __str__(self):
        return f'{self.question.title} - {self.user.first_name}'