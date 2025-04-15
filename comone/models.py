from django.db import models
import uuid

class BaseAnsweres(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    question = models.ForeignKey('sondage.Question',on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Base(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    create_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

