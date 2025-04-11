from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


from .models import User
from .sender_mail import send_mail_user

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True,max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class':'form-control'})
                                 )
    last_name = forms.CharField(required=True,max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,max_length=30,
                             widget=forms.TextInput(
                                 attrs={'class':'form-control','type':'email'}))
    password1 = forms.CharField(required=True,max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(required=True,max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class':'form-control','type':'password'}))
    # role = forms.ChoiceField(required=True,
    #                          widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','role','password1','password2',)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email= email).exists():
            raise ValidationError('Erreur un compte deja associer à ce mail')
        return email
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2') 
        if not password1 or not password2:
            raise ValidationError('le champ mot de passe ne peux pas etre vide')
        if password1 != password2:
            raise ValidationError('les mots de passe ne se correspondent pas')
        return password2
 
    
class ConnexionForm(AuthenticationForm):
        
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(self.request,username = email, password= password)
        if not user:
            raise ValidationError('Email ou mot de pass incorect veillez saisir les bonnes informations')
        if not user.is_active:
            send_mail_user(user)
            raise ValidationError('Votre compte nest pas activer veillez consulter votre boite mail' 
                                  'un message vous a été envoyer pour activer le compte')
        return self.cleaned_data
    
