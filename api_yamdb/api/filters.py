from django_filters.rest_framework import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = CharFilter(field_name='year', lookup_expr='exact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'genre',
            'category',
        )
