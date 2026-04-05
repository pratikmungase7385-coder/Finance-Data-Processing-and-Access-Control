from django.contrib import admin
from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'category', 'amount', 'date', 'created_by', 'is_deleted']
    list_filter = ['transaction_type', 'category', 'is_deleted', 'date']
    search_fields = ['description', 'category']
    ordering = ['-date']
    date_hierarchy = 'date'
