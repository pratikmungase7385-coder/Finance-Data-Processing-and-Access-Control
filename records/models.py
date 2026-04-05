"""
Financial Records model.
Represents income/expense entries with category, date, and notes.
"""
from django.db import models
from django.utils import timezone
from users.models import User


class TransactionType(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'


class Category(models.TextChoices):
    SALARY = 'salary', 'Salary'
    INVESTMENT = 'investment', 'Investment'
    FREELANCE = 'freelance', 'Freelance'
    RENT = 'rent', 'Rent'
    UTILITIES = 'utilities', 'Utilities'
    FOOD = 'food', 'Food & Dining'
    TRANSPORT = 'transport', 'Transport'
    HEALTHCARE = 'healthcare', 'Healthcare'
    ENTERTAINMENT = 'entertainment', 'Entertainment'
    EDUCATION = 'education', 'Education'
    TAX = 'tax', 'Tax'
    OTHER = 'other', 'Other'


class FinancialRecord(models.Model):
    """
    A single financial transaction (income or expense).
    Created and managed by Admin users. Readable by all authenticated users.
    """
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text='Transaction amount (always positive).'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        help_text='Income or Expense.'
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.OTHER,
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='records_created',
    )
    is_deleted = models.BooleanField(default=False)  # Soft delete flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial_records'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['transaction_type']),
            models.Index(fields=['category']),
            models.Index(fields=['date']),
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f'{self.transaction_type.upper()} | {self.category} | {self.amount} on {self.date}'
