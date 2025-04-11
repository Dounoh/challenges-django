from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class CustomeUser(BaseUserManager):
    def create_user(self,first_name,last_name,email,password,**extra_fields):
        if not email:
            raise ValueError('Entrez un mail valide sil vous plait')
        
        user = self.model(first_name = first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,first_name,last_name,email,password,**extrat_fields):
        extrat_fields.setdefault('is_active',False)
        extrat_fields.setdefault('is_staff',False)
        extrat_fields.setdefault('is_superuser',False)
        return self.create_user(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                password=password)
        