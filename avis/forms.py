from __future__ import annotations

from django import forms

from .models import Commentaire
from .models import Critique


class CritiqueForm(forms.ModelForm):
    title = forms.CharField(label='Titre', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=250, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Critique
        fields = ('title', 'description', 'note',)
        widget = {
            'note': forms.Select(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='Commentaire', max_length=50,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Commentaire
        fields = ('comment',)
