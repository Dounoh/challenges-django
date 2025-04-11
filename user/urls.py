from django.urls import path

from .views import CreateUserView,ActivationAccountView,ConnexionView
app_name = 'user'

urlpatterns = [
    path('register/',CreateUserView.as_view(),name='register'),
    path('activation-account/<str:uid>/<str:token>',ActivationAccountView.as_view(),name='activation_account'),
    path('login/',ConnexionView.as_view(),name='login'),
]