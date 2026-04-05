"""
Management command: seed_data
Creates sample users (admin/analyst/viewer) and financial records for testing.

Usage:
    python manage.py seed_data
"""
import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from users.models import User, Role
from records.models import FinancialRecord, TransactionType, Category


SAMPLE_RECORDS = [
    # Incomes
    (Decimal('85000.00'), TransactionType.INCOME, Category.SALARY, 'Monthly salary - March'),
    (Decimal('12500.00'), TransactionType.INCOME, Category.FREELANCE, 'Web design project'),
    (Decimal('5000.00'), TransactionType.INCOME, Category.INVESTMENT, 'Mutual fund returns'),
    (Decimal('3200.00'), TransactionType.INCOME, Category.INVESTMENT, 'Dividend income'),
    (Decimal('78000.00'), TransactionType.INCOME, Category.SALARY, 'Monthly salary - February'),
    (Decimal('9800.00'), TransactionType.INCOME, Category.FREELANCE, 'Consulting fee'),
    # Expenses
    (Decimal('22000.00'), TransactionType.EXPENSE, Category.RENT, 'Monthly apartment rent'),
    (Decimal('4500.00'), TransactionType.EXPENSE, Category.FOOD, 'Groceries and dining'),
    (Decimal('1800.00'), TransactionType.EXPENSE, Category.UTILITIES, 'Electricity and internet'),
    (Decimal('3200.00'), TransactionType.EXPENSE, Category.TRANSPORT, 'Fuel and cab rides'),
    (Decimal('8500.00'), TransactionType.EXPENSE, Category.HEALTHCARE, 'Health insurance premium'),
    (Decimal('2100.00'), TransactionType.EXPENSE, Category.ENTERTAINMENT, 'Streaming and outings'),
    (Decimal('15000.00'), TransactionType.EXPENSE, Category.EDUCATION, 'Online course subscription'),
    (Decimal('12000.00'), TransactionType.EXPENSE, Category.TAX, 'Advance tax payment'),
    (Decimal('900.00'), TransactionType.EXPENSE, Category.OTHER, 'Miscellaneous expenses'),
]


class Command(BaseCommand):
    help = 'Seeds the database with sample users and financial records.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # Create users
        admin_user, _ = User.objects.get_or_create(
            email='admin@finance.com',
            defaults={'full_name': 'Admin User', 'role': Role.ADMIN, 'is_staff': True}
        )
        admin_user.set_password('admin@123')
        admin_user.save()

        analyst_user, _ = User.objects.get_or_create(
            email='analyst@finance.com',
            defaults={'full_name': 'Analyst User', 'role': Role.ANALYST}
        )
        analyst_user.set_password('analyst@123')
        analyst_user.save()

        viewer_user, _ = User.objects.get_or_create(
            email='viewer@finance.com',
            defaults={'full_name': 'Viewer User', 'role': Role.VIEWER}
        )
        viewer_user.set_password('viewer@123')
        viewer_user.save()

        self.stdout.write(self.style.SUCCESS('  ✓ Users created'))

        # Create financial records across the last 90 days
        today = date.today()
        for i, (amount, t_type, category, description) in enumerate(SAMPLE_RECORDS):
            record_date = today - timedelta(days=random.randint(0, 90))
            FinancialRecord.objects.get_or_create(
                amount=amount,
                transaction_type=t_type,
                category=category,
                date=record_date,
                defaults={'description': description, 'created_by': admin_user}
            )

        self.stdout.write(self.style.SUCCESS('  ✓ Financial records created'))
        self.stdout.write(self.style.SUCCESS('\nSeed complete!\n'))
        self.stdout.write('Test credentials:')
        self.stdout.write('  Admin   → admin@finance.com    / admin@123')
        self.stdout.write('  Analyst → analyst@finance.com  / analyst@123')
        self.stdout.write('  Viewer  → viewer@finance.com   / viewer@123')
