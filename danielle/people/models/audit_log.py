from django.db import models


class AuditLog(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    ACTION_CHOICES = [
        (ACTION_CREATE, "Criação"),
        (ACTION_UPDATE, "Atualização"),
        (ACTION_DELETE, "Exclusão"),
    ]

    action = models.CharField(max_length=12, choices=ACTION_CHOICES)
    entity = models.CharField(max_length=80)
    object_id = models.PositiveIntegerField()
    changed_fields = models.JSONField(default=list, blank=True)
    before_data = models.JSONField(null=True, blank=True)
    after_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de auditoria"
        verbose_name_plural = "Logs de auditoria"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entity", "object_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.entity}#{self.object_id} - {self.action}"
