from __future__ import annotations

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User
from .send_mail import sender_mail


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prenom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        max_length=30, required=True, label='mot de pass', widget=forms.PasswordInput())
    password2 = forms.CharField(
        max_length=30, required=True, label='Confirmation', widget=forms.PasswordInput())
    profil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password1', 'password2', 'role', 'profil')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Erreur un compte est deja associer à mail')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError(
                'Champ obligatoire le champ mot de pass doit etre rempli')

        if password1 != password2:
            raise ValidationError('les deux mot de pass ne se ressemble pas')
        return password2


class CustomeAuthenticate(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(self.request, username=email, password=password)
        if user is None:
            raise ValidationError('Les informations saisies sont incorectes')

        if not user.is_active:
            sender_mail(user)
            raise ValidationError('Votre compte n\'est pas activer veillez consulter'
                                  'votre boite mail pour activer votre compte.')

        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Erreur aucun compte associer à ce mail')
        return email


class NewPasswordForm(forms.Form):
    password1 = forms.CharField(label='Nouveau mot de pass :', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmation :', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError(
                'le champ mot de pass ne doit pas etre vide.')
        if password1 != password2:
            raise ValidationError('les deux mots de pass sont differents')

        if len(password2) < 5:
            raise ValidationError(
                'le mot de pass doit etre supperieur à 5 elements')
        if not any(digi.isdigit() for digi in password2):
            raise ValidationError(
                'le mot de pass doit contenir au moin un chiffre')
        if not any(char.isalpha() for char in password2):
            raise ValidationError(
                'le mot de pass doit contenir au moin une lettre')
        if not any(up.isupper() for up in password2):
            raise ValidationError(
                'le mot de pass doit contenir au moin une lettre majuscule')
        if not any(low.islower() for low in password2):
            raise ValidationError(
                'le mot de pass doit contenir au moin une lettre miniscule')

        return password2


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "role", "email", "profil",)
