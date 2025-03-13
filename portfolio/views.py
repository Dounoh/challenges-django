from django.shortcuts import render
from .models import UserInfos,Experiences,Competences,Realisation,Contact
from django.views import View

class ViewPortfolio(View):
    def get(self,request):
        userInfos = UserInfos.objects.all().first()
        experiences = Experiences.objects.all()
        competences = Competences.objects.all()
        realisations = Realisation.objects.all()
        context = {
            'userInfos': userInfos,
            'experiences': experiences,
            'competences': competences,
            'realisations': realisations,
        }
        return render(request,'portfolio/index.html',context)