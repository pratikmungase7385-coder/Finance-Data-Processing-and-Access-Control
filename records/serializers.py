"""
Serializers for FinancialRecord model.
"""
from rest_framework import serializers
from decimal import Decimal
from .models import FinancialRecord, TransactionType, Category
from users.serializers import UserSerializer


class FinancialRecordSerializer(serializers.ModelSerializer):
    """Full serializer for reading records."""
    created_by = UserSerializer(read_only=True)
    transaction_type_display = serializers.CharField(
        source='get_transaction_type_display', read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = FinancialRecord
        fields = [
            'id', 'amount', 'transaction_type', 'transaction_type_display',
            'category', 'category_display', 'date', 'description',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class CreateUpdateRecordSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating financial records."""

    class Meta:
        model = FinancialRecord
        fields = ['amount', 'transaction_type', 'category', 'date', 'description']

    def validate_amount(self, value):
        if value <= Decimal('0'):
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def validate_transaction_type(self, value):
        valid = [t.value for t in TransactionType]
        if value not in valid:
            raise serializers.ValidationError(
                f'transaction_type must be one of: {", ".join(valid)}'
            )
        return value

    def validate_category(self, value):
        valid = [c.value for c in Category]
        if value not in valid:
            raise serializers.ValidationError(
                f'category must be one of: {", ".join(valid)}'
            )
        return value
