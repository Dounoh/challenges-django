from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from .managers import CustomeUser

choise_role = {
    'realisateur': 'Realisateur',
    'utilisateur': 'Utilisateur',
}


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profil = models.ImageField(upload_to='media/user/', null=True, blank=True)
    role = models.CharField(max_length=12, blank=False,
                            choices=choise_role, null=False)
    username = None

    objects = CustomeUser()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
