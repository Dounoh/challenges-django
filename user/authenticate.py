from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomeAuthenticate(ModelBackend):
    print('ma class est appeler')
    def authenticate(self,request,username,password):
        print('je commence')
        try:
            user = User.objects.get(email = username)
            print('je filtre le user')
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            request.user = user
            return user
        return None