from people.models import Checkout
from people.serializers import CheckoutSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class CheckoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar check-outs.
    Criar um checkout marca o check-in associado como inativo.
    """
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
