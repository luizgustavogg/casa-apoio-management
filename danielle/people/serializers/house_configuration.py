from people.models import HouseConfiguration
from rest_framework import serializers


class HouseConfigurationSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.SerializerMethodField()
    available_vacancies = serializers.SerializerMethodField()
    is_at_full_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = HouseConfiguration
        fields = [
            'id',
            'max_capacity',
            'current_occupancy',
            'available_vacancies',
            'is_at_full_capacity',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'current_occupancy',
            'available_vacancies',
            'is_at_full_capacity',
            'created_at',
            'updated_at'
        ]
    
    def get_current_occupancy(self, obj):
        """Retorna o número de check-ins ativos."""
        return HouseConfiguration.get_current_occupancy()
    
    def get_available_vacancies(self, obj):
        """Retorna o número de vagas disponíveis."""
        return HouseConfiguration.get_available_vacancies()
    
    def get_is_at_full_capacity(self, obj):
        """Retorna se está em capacidade máxima."""
        return HouseConfiguration.is_at_full_capacity()
