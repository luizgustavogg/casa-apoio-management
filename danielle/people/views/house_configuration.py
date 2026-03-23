from people.models import HouseConfiguration
from people.serializers import HouseConfigurationSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class HouseConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar a configuração da casa de apoio.
    Fornece informações sobre capacidade máxima e ocupação atual.
    """
    queryset = HouseConfiguration.objects.all()
    serializer_class = HouseConfigurationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def occupancy_status(self, request):
        """
        Endpoint que retorna o status de ocupação da casa.
        GET /api/v1/house-configuration/occupancy_status/
        """
        config = HouseConfiguration.get_config()
        serializer = self.get_serializer(config)
        return Response(serializer.data)
