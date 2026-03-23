from people.models import ProfessionalServices
from rest_framework import serializers


class ProfessionalServicesSerializer(serializers.ModelSerializer):
    professional_name = serializers.CharField(required=False)
    formatted_created_at = serializers.CharField(required=False)

    class Meta:
        model = ProfessionalServices
        exclude = ['updated_at', 'created_at']
        extra_kwargs = {'professional_name': {'read_only': True}}
