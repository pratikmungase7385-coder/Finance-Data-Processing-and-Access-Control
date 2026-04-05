
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import FinancialRecord
from .serializers import FinancialRecordSerializer, CreateUpdateRecordSerializer
from .filters import FinancialRecordFilter
from users.permissions import IsAdminOrReadOnly, IsAnyRole


class FinancialRecordListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/records/   → All authenticated users: list records (paginated, filterable)
    POST /api/records/   → Admin only: create a new record
    """
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FinancialRecordFilter
    search_fields = ['description', 'category']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        # Exclude soft-deleted records
        return FinancialRecord.objects.filter(is_deleted=False).select_related('created_by')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateRecordSerializer
        return FinancialRecordSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save(created_by=request.user)
        return Response(
            FinancialRecordSerializer(record).data,
            status=status.HTTP_201_CREATED
        )


class FinancialRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/records/<id>/  → All authenticated users
    PATCH  /api/records/<id>/  → Admin only
    DELETE /api/records/<id>/  → Admin only (soft delete)
    """
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return FinancialRecord.objects.filter(is_deleted=False).select_related('created_by')

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CreateUpdateRecordSerializer
        return FinancialRecordSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        record = serializer.save()
        return Response(FinancialRecordSerializer(record).data)

    def destroy(self, request, *args, **kwargs):
        """Soft delete: set is_deleted=True instead of removing from DB."""
        record = self.get_object()
        record.is_deleted = True
        record.save()
        return Response(
            {'detail': f'Record {record.id} has been deleted.'},
            status=status.HTTP_200_OK
        )
