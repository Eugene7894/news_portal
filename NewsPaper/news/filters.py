import django.forms
from django_filters import FilterSet, DateFilter
from .models import Post


# создаём фильтр
class NewsFilter(FilterSet):
    creationDate = DateFilter(lookup_expr='gt', widget=django.forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {'title': ['icontains'], 'author': ['exact']}
