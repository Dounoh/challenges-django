from __future__ import annotations

from django import forms

from .models import Film


class CreateFilmForm(forms.ModelForm):

    class Meta:
        model = Film
        fields = ['title', 'synopsis', 'genre', 'out_date',
                  'casting', 'duree', 'image', 'publie']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'casting': forms.TextInput(attrs={'class': 'form-control'}),
            'duree': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'publie': forms.CheckboxInput(attrs={'class': 'btn-outline-primary'}),
        }
