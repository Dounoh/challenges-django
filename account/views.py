from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.db import transaction
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.core.exceptions import ValidationError

from .forms import CustomAuthenticateForm,CustomiseUserForm,ForgotPasswordForm
from .forms import NewPasswordForm
from .send_mail import sender_mail,sender_mail_password


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticateForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('accueil')
    
class CreateUer(CreateView):
    form_class = CustomiseUserForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            sender_mail(user)
        messages.success(self.request,'Votre compte a ete cree avec succes. '
                             'Un message de confirmation vous a été envoyer sur votre mail.')
        return redirect('login')


class Activation_account(View):
    redirection = reverse_lazy('login')
    
    def get(self,request,uid,token):
        id = urlsafe_base64_decode(uid)

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return render(request=request,template_name='account/invalid_validation.html')
        
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(self.request,'Votre compte a été activé avec success')
            return redirect(self.redirection)
            
        return render(request=request,template_name='account/invalid_validation.html')
        
            

class ForgotPassword(View):
    
    def get(self,request):
        form = ForgotPasswordForm()
        return render(request,'account/forgot_password.html',{'form':form})
    
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # Utilise cleaned_data pour obtenir l'email
            try:
                user = User.objects.get(email=email)
                sender_mail_password(user)  # Envoie l'email de réinitialisation
                messages.success(request, 'Un email vous a été envoyé pour réinitialiser votre mot de passe.')
                return redirect('login')  # Redirige vers la page de connexion
            except User.DoesNotExist:
                # Gérer le cas où l'utilisateur n'existe pas
                messages.error(request, 'Cet utilisateur n\'existe pas, veuillez entrer des informations valides.')
                return render(request, 'account/forgot_password.html', {'form': form})
        else:
            messages.error(request,'entrez un champ valide')
            
        
def new_password(request,uid,token):
    id = urlsafe_base64_decode(uid)
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return render(request=request,template_name='account/invalid_validation.html')

    if not default_token_generator.check_token(user,token):
        return render(request=request,template_name='account/invalid_validation.html')

    form = NewPasswordForm()

    if request.method =='POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('password2')
            with transaction.atomic():
                user.set_password(new_password)
                user.save()
            messages.success(request,'le mot de pass a été changer avec success')
            return redirect('login')
    
    return render(request,'account/new_password.html',{'form':form})

def deconnexion(request):
    logout(request)
    return redirect('login')