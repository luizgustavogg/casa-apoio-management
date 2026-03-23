from people.models import Checkin
from rest_framework import serializers

from people.models import PatientCompanionCheckin


class CheckinSerializer(serializers.ModelSerializer):
    companion_name = serializers.CharField(required=False, allow_blank=True)
    person_name = serializers.CharField(required=False, allow_blank=True)
    formatted_created_at = serializers.CharField(required=False,
                                                 allow_blank=True)

    def validate(self, data):
        # check if patient have a companion
        if data['reason'] == 'patient':
            if 'companion' not in data.keys():
                raise serializers.ValidationError(
                    {'companion': 'Todo paciente deve ter acompanhante.'})
            else:
                if not data['companion']:
                    raise serializers.ValidationError(
                        {'companion': 'Campo acompanhante não pode ser nulo.'})
        
        # check house capacity
        from people.models import HouseConfiguration
        if HouseConfiguration.is_at_full_capacity():
            raise serializers.ValidationError(
                {'detail': 'Casa de apoio em capacidade máxima. Não há vagas disponíveis no momento.'})
        
        return data

    class Meta:
        model = Checkin
        exclude = ['updated_at', 'created_at']
        read_only_fields = ('companion_name', 'person_name',
                            'formatted_created_at')


class PatientCompanionCheckinSerializer(serializers.ModelSerializer):
    companion_name = serializers.CharField(required=False, allow_blank=True)
    patient_name = serializers.CharField(required=False, allow_blank=True)
    formatted_created_at = serializers.CharField(required=False,
                                                 allow_blank=True)

    class Meta:
        model = PatientCompanionCheckin
        exclude = ['updated_at', 'created_at']
        read_only_fields = ('companion_name', 'patient_name',
                            'formatted_created_at')