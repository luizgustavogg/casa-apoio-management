from people.models import Person
from rest_framework import serializers
from utils.string.format_text import format_text


class PersonSerializer(serializers.ModelSerializer):
    formatted_born_date = serializers.CharField(required=False)
    formatted_cpf = serializers.CharField(required=False)
    formatted_postal_code = serializers.CharField(required=False)

    def to_internal_value(self, data):
        fields_to_format = [
            'city', 'name', 'mother_name', 'address_line_1', 'address_line_2',
            'neighbourhood'
        ]
        for field in fields_to_format:
            if field in data.keys():
                if data[field]:
                    data[field] = format_text(data[field])
        return super().to_internal_value(data)

    class Meta:
        model = Person
        fields = "__all__"
        extra_kwargs = {
            'formatted_born_date': {
                'read_only': True
            },
            'formatted_cpf': {
                'read_only': True
            }
        }
