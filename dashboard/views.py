from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from records.models import FinancialRecord, TransactionType
from users.permissions import IsAnalystOrAdmin, IsAnyRole



def _base_qs():
    return FinancialRecord.objects.filter(is_deleted=False)


# =========================
# OVERVIEW
# =========================
class OverviewView(APIView):
    permission_classes = [IsAnalystOrAdmin]

    def get(self, request):
        qs = _base_qs()

        # 🔥 FILTER
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if start:
            qs = qs.filter(date__gte=parse_date(start))
        if end:
            qs = qs.filter(date__lte=parse_date(end))

        totals = qs.aggregate(
            total_income=Sum('amount', filter=Q(transaction_type=TransactionType.INCOME)),
            total_expenses=Sum('amount', filter=Q(transaction_type=TransactionType.EXPENSE)),
        )

        income = totals['total_income'] or 0
        expense = totals['total_expenses'] or 0

        return Response({
            "total_income": income,
            "total_expenses": expense,
            "net_balance": income - expense
        })


# =========================
# CATEGORY BREAKDOWN (PIE)
# =========================
class CategoryBreakdownView(APIView):
    permission_classes = [IsAnalystOrAdmin]

    def get(self, request):
        qs = _base_qs()

        # 🔥 FILTER
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if start:
            qs = qs.filter(date__gte=parse_date(start))
        if end:
            qs = qs.filter(date__lte=parse_date(end))

        breakdown = (
            qs.values('category', 'transaction_type')
            .annotate(total=Sum('amount'))
        )

        result = {}
        for row in breakdown:
            cat = row['category']
            if cat not in result:
                result[cat] = 0
            if row['transaction_type'] == TransactionType.EXPENSE:
                result[cat] += float(row['total'])

        formatted = [
            {"category": k, "expense": v}
            for k, v in result.items()
        ]

        return Response({"categories": formatted})


# =========================
# MONTHLY TREND (LINE)
# =========================
class MonthlyTrendsView(APIView):
    permission_classes = [IsAnalystOrAdmin]

    def get(self, request):
        qs = _base_qs()

       
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if start:
            qs = qs.filter(date__gte=parse_date(start))
        if end:
            qs = qs.filter(date__lte=parse_date(end))

        monthly = (
            qs.annotate(month=TruncMonth('date'))
            .values('month', 'transaction_type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        result = {}
        for row in monthly:
            key = row['month'].strftime('%Y-%m')
            if key not in result:
                result[key] = {'month': key, 'income': 0, 'expense': 0}
            result[key][row['transaction_type']] = float(row['total'])

        trends = list(result.values())

        return Response({"trends": trends})


# =========================
# RECENT ACTIVITY (TABLE)
# =========================
class RecentActivityView(APIView):
    permission_classes = [IsAnyRole]

    def get(self, request):
        qs = _base_qs().order_by('-date')[:10]

        data = [
            {
                "id": r.id,
                "amount": float(r.amount),
                "transaction_type": r.transaction_type,
                "category": r.category,
                "date": r.date
            }
            for r in qs
        ]

        return Response({"records": data})