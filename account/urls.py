from django.urls import path
from .views import CustomLoginView,CreateUer,Activation_account
from .views import ForgotPassword,new_password,deconnexion
urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('inscription/',CreateUer.as_view(),name='inscription'),
    path('activation-mail/<uid>/<token>/',Activation_account.as_view(),name='activation_account'),
    path('deconnexion/',deconnexion,name='deconnexion'),
    
    path('mot-de-pass-oublier/',ForgotPassword.as_view(),name='forgot_password'),
    path('nouveau-password/<uid>/<token>/',new_password,name='new_password'),
    
]