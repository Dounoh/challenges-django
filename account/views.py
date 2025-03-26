from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView

from .forms import CreateUserForm
from .forms import CustomeAuthenticate
from .forms import ForgotPasswordForm
from .forms import NewPasswordForm
from .forms import UpdateUserForm
from .models import User
from .send_mail import sender_mail
from .send_mail import sender_mail_reset_password


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')
    context_object_name = 'form'

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sender_mail(user)
        messages.success(self.request, 'votre compte a été cree avec succes.'
                         'veillez consulter votre mail pour activer votre compte')
        return redirect(self.success_url)


class ConnexionView(LoginView):
    authentication_form = CustomeAuthenticate
    template_name = 'account/login.html'
    success_url = reverse_lazy('movie:film_view')

    def get_success_url(self):
        return self.success_url


def deconnexion(request):
    logout(request)
    return redirect('movie:film_view')


class ActivationAccountView(View):
    redic = reverse_lazy('account:login')

    def get(self, request, uid, token):

        id = urlsafe_base64_decode(uid)
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return render(request, 'account/activation_error.html')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Votre compte a été activer avec succes')
            return redirect(self.redic)

        return render(request, 'account/activation_error.html')


class ForgotPasswordView(View):

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'account/password_forgot.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                sender_mail_reset_password(user)
                messages.success(
                    request, 'Un mail de reinitialisation vous a ete envoyer avec succes')
                return redirect('account:login')
            except User.DoesNotExist:
                raise ValueError('aucun compte associer a ce mail')
        else:
            return render(request, 'account/password_forgot.html', {'form': form})


def new_password(request, uid, token):
    redic = reverse_lazy('account:login')
    form = NewPasswordForm()

    id = urlsafe_base64_decode(uid)
    try:
        user = User.objects.get(pk=id)
        print(f"Utilisateur trouvé : {user.email}")
    except User.DoesNotExist:
        print(f"Erreur lors du décodage de l'UID ou utilisateur non trouvé :")
        return render(request, 'account/activation_error.html')

    if not default_token_generator.check_token(user, token):
        print("Token invalide ou expiré")
        return render(request, 'account/activation_error.html')

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password2')
            user.set_password(password)
            user.save()
            messages.success(request, 'Mot de pass modifier avec succes.')
            return redirect(redic)

    return render(request=request,
                  template_name='account/new_password.html',
                  context={'form': form})


class ProfilView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'account/profil.html', context)


class DeleteAccountView(View):
    redirect_url = reverse_lazy('movie:film_view')

    def get(self, request):
        with transaction.atomic():
            user = request.user
            user.delete()
        messages.success(request, 'compte supprimer avec succes')
        return redirect(self.redirect_url)


class EditProfilView(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'account/edit_profil.html'
    success_url = reverse_lazy('account:profil')

    def form_valid(self, form):
        messages.success(
            self.request, 'Votre profil a été modifier avec success')
        return super().form_valid(form)
