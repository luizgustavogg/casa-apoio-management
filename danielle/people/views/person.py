from people.models import Person
from people.serializers import PersonSerializer
from django.db.models import ProtectedError
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {
                    "detail": "Não é possível excluir esta pessoa porque ela possui registros vinculados (ex.: check-ins)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
