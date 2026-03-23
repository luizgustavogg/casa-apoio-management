from people.models import ProfessionalServices
from people.serializers import ProfessionalServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class ProfessionalServicesViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalServices.objects.all()
    serializer_class = ProfessionalServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['professional__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]