from django.db import models
import uuid
from sondage.models import Question,Survey,Response,Proposed
from comone.models import Base, BaseAnsweres

#Réponse du participant à la question (soit choix, soit texte)
    
class AnswersUnique(BaseAnsweres):
    answer = models.ForeignKey(Proposed,on_delete=models.CASCADE)

class AnswersMultiple(BaseAnsweres):
    answer = models.ManyToManyField(Proposed)

class AnswersText(BaseAnsweres):
    answer = models.ForeignKey(Proposed,on_delete=models.CASCADE)
    text = models.CharField(max_length=200)



