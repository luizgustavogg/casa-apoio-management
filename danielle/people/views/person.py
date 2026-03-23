from people.models import Person
from people.serializers import PersonSerializer
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]
