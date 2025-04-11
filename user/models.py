from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

from .managers import CustomeUser

ROLE_USER = [
    ('creator','creator',),
    ('participant','participant',)
]

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30,null=False)
    last_name = models.CharField(max_length=30,null=False)
    email = models.EmailField(unique=True,null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=12,choices=ROLE_USER, null=False, default='participant')
    username = None
    
    objects = CustomeUser()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','password']
    EMAIL_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm, obj= None):
        return True
    
    def has_modul_perm(self,app_label):
        return True