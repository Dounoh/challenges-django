from django import forms
from django.forms import modelformset_factory,inlineformset_factory
from .models import Survey, Choice, Question, Proposed

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title_survey', 'description', 'start_date', 'end_date',)
        widgets = {
            'title_survey': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}),  
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class QuestionForm(forms.ModelForm):
    title_question = forms.CharField(label='Question', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Question
        fields = ('title_question', 'choice',)
        widgets = {
            'choice': forms.Select(attrs={'class': 'form-control'}),
        }


class ProposedForm(forms.ModelForm):
    class Meta:
        model = Proposed
        fields = ('response',)
        widgets = {
            'response' : forms.TextInput(attrs={'class': 'form-control'})
        }

ProposedFromSet = inlineformset_factory(Question, Proposed,  form= ProposedForm , extra=1)

# class ChoiseForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ('answer_text',)

# # Créer un formset pour le modèle Choice lié à Question
# ChoiceFormSet = modelformset_factory(Choice,fields = ('answer_text',), extra=1)
