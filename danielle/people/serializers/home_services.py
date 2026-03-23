from people.models import HomeServices
from rest_framework import serializers


class HomeServicesSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(required=False)
    formatted_created_at = serializers.CharField(required=False)

    class Meta:
        model = HomeServices
        exclude = ['updated_at', 'created_at']
        extra_kwargs = {'person_name': {'read_only': True}}