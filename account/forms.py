from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .send_mail import sender_mail


class CustomiseUserForm(UserCreationForm):
    email = forms.EmailField(required=True,max_length=30)
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Mot de pass',help_text='champ obligatoire')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmation',help_text='champ obligatoire')

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password1','password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError('Le mail exist deja')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('les deux mot de pass sont different')
        else:
            raise ValidationError('le champ mot de pass est obligatoire')
        
        return password2
    
class CustomAuthenticateForm(AuthenticationForm):
        
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user =  authenticate(self.request, username=email,password=password)
        if user is None:
            raise ValidationError('Informations incorrecte')
        if not user.is_active:
            sender_mail(user)
            raise ValidationError('votre compte n\'est pas activer veillez '
                                  'consulter votre boite mail pour activer le compte')
       
        return self.cleaned_data
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email = email).exists():
            raise ValidationError('cet utilisateur n\'existe pas veillez entrez des bonnes informations')
        return email
    
class NewPasswordForm(forms.Form):
    password1 = forms.CharField(required=True,label='Mot de pass:',widget=forms.PasswordInput())
    password2 = forms.CharField(required=True,label='Confirmation:',widget=forms.PasswordInput())
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if len(password1) < 5:
            raise ValidationError('le mot de pass doit etre supperieur a 5 elements')
        
        if not any(num.isdigit() for num in password1):
            raise ValidationError('le mot de pass doit contenir au moin un chiffre')
        
        if not any(char.isalpha() for char in password1):
            raise ValidationError('le mot de pass doit contenir au moin une lettre')
        
        if not any(up.isupper() for up in password1):
            raise ValidationError('le mot de pass doit contenir au moin une majuscule.')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Les deux mot de pass se ressemblent pas.')
        else:
            raise ValidationError('le champs mot de passe ne peut pas etre vide.')
        
        return password2