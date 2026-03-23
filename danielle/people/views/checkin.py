from people.models import Checkin
from people.models import PatientCompanionCheckin
from people.serializers import CheckinSerializer
from people.serializers import PatientCompanionCheckinSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class CheckinViewSet(viewsets.ModelViewSet):
    queryset = Checkin.objects.all()
    serializer_class = CheckinSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['person__name']
    filterset_fields = ['active']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]


class PatientCompanionCheckinViewSet(viewsets.ModelViewSet):
    queryset = PatientCompanionCheckin.objects.all()
    serializer_class = PatientCompanionCheckinSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['patient__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]
