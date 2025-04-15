from django import forms 

from .models import AnswersText, AnswersMultiple, AnswersUnique

class AnswersText(forms.ModelForm):
    class Meta:
        model = AnswersText
        fields = ('text')