from django.urls import path
from .views import index,index1,CreateSurveyView

app_name = 'admin-survey'
urlpatterns = [
    path('',index,name='dashbord'),
    path('add/',CreateSurveyView.as_view(),name='add'),
    path('create/',CreateSurveyView.as_view(),name='create'),
]
