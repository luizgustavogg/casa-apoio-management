from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Atualizado em")

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%d/%m/%Y")

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%d/%m/%Y")

    class Meta:
        abstract = True
