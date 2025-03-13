from django.contrib.auth.models import BaseUserManager


class Usermanager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password, **extra_fields):
        
        if not email:
            raise ValueError('email doit etre renseigner.')
        
        user = self.model(email = email,
                          first_name = first_name,
                          last_name = last_name,
                          **extra_fields
                          )
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,email,first_name,last_name,password, **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email,
                                last_name=last_name,
                                first_name=first_name,
                                password=password,
                                **extra_fields)
        