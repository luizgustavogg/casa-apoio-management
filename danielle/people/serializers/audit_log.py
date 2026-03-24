from rest_framework import serializers

from people.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = (
            "id",
            "action",
            "entity",
            "object_id",
            "changed_fields",
            "before_data",
            "after_data",
            "created_at",
        )
