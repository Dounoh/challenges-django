from django.db import models
from django.utils import timezone
from account.models import User


class UserInfos(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    profession = models.CharField(max_length=40,null=False,blank=False)
    about = models.TextField(verbose_name='a propos')
    image = models.ImageField(upload_to='media/userInfos/')
    linkcv = models.CharField(max_length=100)
    date_at = models.DateField(default=timezone.now)
    
    
class Competences(models.Model):
    title = models.CharField(max_length=40)
    progress = models.FloatField(default=0.0)
    
class Experiences(models.Model):
    image = models.ImageField(upload_to='media/experiences/',null=True,blank=True)
    title = models.CharField(max_length=40,null=False,blank=True)
    description = models.TextField(max_length=200)
    
class Realisation(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='media/realisations',null=True,blank=True)
    link = models.CharField(max_length=40)
    

class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    objet = models.CharField(max_length=30)
    messages =  models.TextField(max_length=200)
    date_at = models.DateField(default=timezone.now)

