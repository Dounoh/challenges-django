
import django_filters
from .models import Film
from django.db.models import Avg

class FilmFilter(django_filters.FilterSet):
    out_date = django_filters.DateFilter(field_name='out_date', lookup_expr='exact', label="Date de sortie")
    note_moyenne = django_filters.NumberFilter(method='filter_note_moyenne', label="Note Moyenne")

    class Meta:
        model = Film
        fields = ['genre', 'out_date']

    def filter_note_moyenne(self, queryset, name, value):
        return queryset.annotate(avg_note=Avg('critiques__note')).filter(avg_note__gte=value)


#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     # Créer une liste de choix pour le genre
#     #     self.filters['out_date'].choices = [(out_date, out_date) for out_date in Film.objects.values_list('out_date', flat=True).distinct()]
    