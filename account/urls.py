from __future__ import annotations

from django.urls import path

from .views import ActivationAccountView
from .views import ConnexionView
from .views import CreateUserView
from .views import deconnexion
from .views import DeleteAccountView
from .views import EditProfilView
from .views import ForgotPasswordView
from .views import new_password
from .views import ProfilView

app_name = 'account'
urlpatterns = [
    path('login/', ConnexionView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('activation/<uid>/<token>',
         ActivationAccountView.as_view(), name='activation'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('new-password/<uid>/<token>', new_password, name='new_password'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('profil/', ProfilView.as_view(), name='profil'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('Edit-profil/<int:pk>/', EditProfilView.as_view(), name='edit_profil'),
]
