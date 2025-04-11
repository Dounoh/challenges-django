from django import forms
from django.forms import modelformset_factory,inlineformset_factory
from sondage.models import Survey, Choice, Question

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title_survey', 'description', 'start_date', 'end_date',)
        widgets = {
            'title_survey': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Correction du widget
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title_question', 'type_answer',)

class ChoiseForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('answer_text',)

# Créer un formset pour le modèle Choice lié à Question
ChoiceFormSet = modelformset_factory(Choice,fields = ('answer_text',), extra=1)
