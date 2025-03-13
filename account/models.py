from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from .managers import Usermanager


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30,blank=False,null=False)
    last_name = models.CharField(max_length=30,blank=False,null=False)
    email = models.EmailField(unique=True,null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = None
    
    objects = Usermanager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name','first_name','password']
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Logique pour vérifier les permissions (peut être personnalisé)
        return True  # Ajustez selon vos besoins

    def has_module_perms(self, app_label):
        # Logique pour vérifier les permissions de module
        return True  # Ajustez selon vos besoins