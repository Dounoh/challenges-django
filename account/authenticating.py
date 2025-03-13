from django.contrib.auth.backends import ModelBackend
from account.models import User

class CustomAuthenticator(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email =username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            request.user = user
            return user
        return None
    