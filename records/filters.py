"""
Filter set for FinancialRecord queryset.
"""
import django_filters
from .models import FinancialRecord, TransactionType, Category


class FinancialRecordFilter(django_filters.FilterSet):
    # Exact match filters
    transaction_type = django_filters.ChoiceFilter(choices=TransactionType.choices)
    category = django_filters.ChoiceFilter(choices=Category.choices)

    # Date range filters
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    # Amount range filters
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = FinancialRecord
        fields = ['transaction_type', 'category', 'date_from', 'date_to', 'amount_min', 'amount_max']
