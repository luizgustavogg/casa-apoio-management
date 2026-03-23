from people.models import HomeServices
from people.serializers import HomeServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class HomeServicesViewSet(viewsets.ModelViewSet):
    queryset = HomeServices.objects.all()
    serializer_class = HomeServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['person__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]