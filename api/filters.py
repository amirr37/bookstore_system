import django_filters
from django_filters import OrderingFilter

from books.models import Book, City
from django.db.models import Q


class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    genre = django_filters.CharFilter(label='genre', lookup_expr='icontains')
    author_name = django_filters.CharFilter(method='filter_by_author_name', label='Author name')
    city = django_filters.ChoiceFilter(field_name='authors__birthplace', choices=City.objects.values_list('id', 'name'),
                                       label='Author Birthplace')
    ordering = OrderingFilter(fields=(('price', 'Price'),), )

    def filter_by_author_name(self, queryset, name, value):
        return queryset.filter(Q(authors__first_name__icontains=value) | Q(authors__last_name__icontains=value))

    class Meta:
        model = Book
        fields = ['min_price', 'max_price', 'city']
