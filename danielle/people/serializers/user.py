from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import re


class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        if value.isalnum():
            raise serializers.ValidationError(
                'Password deve ter pelo menos um caracter especial.')
        if len(value) < 8:
            raise serializers.ValidationError(
                'Password deve ter pelo 8 caracteres.')
        if not re.findall(r'[A-Z]+', value):
            raise serializers.ValidationError(
                'Password deve ter pelo menos uma letra maiúscula.')
        if not re.findall(r'[0-9]+', value):
            raise serializers.ValidationError(
                'Password deve ter pelo menos um dígito de 0 a 9.')
        return value

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        return representation
