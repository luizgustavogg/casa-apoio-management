from people.models import Checkout
from rest_framework import serializers


class CheckoutSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # check if checkin is active
        if not data['checkin'].active:
            raise serializers.ValidationError({'checkin': 'Checkin inválido.'})
        return data
    
    def create(self, validated_data):
        """Cria o checkout e marca o checkin como inativo."""
        checkout = super().create(validated_data)
        # Desativar o check-in quando o checkout é criado
        checkin = validated_data['checkin']
        checkin.active = False
        checkin.save()
        return checkout

    class Meta:
        model = Checkout
        fields = "__all__"
