from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views import View
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView

from .models import User
from .sender_mail import send_mail_user
from .forms import CreateUserForm,ConnexionForm

class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')
    
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        send_mail_user(user)
        messages.success(self.request,'votre compte a été cree avec succes '
                         'veillez consulter votre boite mail pour l\'activation de votre compte.')
        return redirect(self.success_url)
    
class ActivationAccountView(View):
    redirect_url = reverse_lazy('user:login')
    def get(self,uid,token):
        id = urlsafe_base64_decode(uid)
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return render(request=self.request,template_name='user/invalide_mail.html')
        
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(self.request,'votre compte a été activer avec success')
            return redirect(self.redirect_url)
        
        return render(request=self.request,template_name='user/invalide_mail.html')

class ConnexionView(LoginView):
    authentication_form = ConnexionForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('sondage:')