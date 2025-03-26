from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import User


class CustomeAuthenticator(ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            request.user = user
            return user
        return None


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Appeler l'authentification personnalisée pour récupérer l'utilisateur
        user = super().authenticate(request)

        # Si un utilisateur n'est pas trouvé, tentez de récupérer un utilisateur via le backend personnalisé
        if user is None:
            # ou request.data.get('email') en fonction de votre setup
            email = request.data.get('username')
            try:
                user = get_user_model().objects.get(email=email)
                # Vérifiez le mot de passe
                if user.check_password(request.data.get('password')):
                    return (user, None)
            except User.DoesNotExist:
                return None

        return user
