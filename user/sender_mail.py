from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from config.settings import DOMAINE_URL

def send_mail_user(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    subject = 'Activation de compte'
    context = {
        'user':user,
        'uid':uid,
        'token':token,
        'domaine': DOMAINE_URL
        }
    message = render_to_string(template_name='user/activation_mail.html',context=context)
    send_mail(subject=subject,message=message,
              from_email='dounoh0@gmail.com',
              recipient_list = [user.email],
              fail_silently=False)