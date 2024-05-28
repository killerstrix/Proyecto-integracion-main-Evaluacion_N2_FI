import django_filters
from .models import producto

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = producto
        fields = ['categoria']
