from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from conf.settings import DOMAIN_URL

def sender_mail(user):
    subject = 'Activation de compte'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    context = {
        'uid':uid,
        'token': token,
        'user': user,
        'domaine': DOMAIN_URL,
    }
    message = render_to_string('account/activation_mail.html',context)
    
    send_mail(subject=subject,message=message,from_email='dounoh0@gmail.com',recipient_list=[user.email],fail_silently=False)
    
def sender_mail_password(user):
    subject = 'Changement de mot de pass'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    context = {
        'uid':uid,
        'token': token,
        'user': user,
        'domaine': DOMAIN_URL,
    }
    message = render_to_string('account/mail_password.html',context)
    
    send_mail(subject=subject,message=message,from_email='dounoh0@gmail.com',recipient_list=[user.email],fail_silently=False)