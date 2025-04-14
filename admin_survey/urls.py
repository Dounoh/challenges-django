from django.urls import path
from .views import DashboardView

app_name = 'admin-survey'
urlpatterns = [
    path('',DashboardView.as_view(),name='dashbord'),
]
