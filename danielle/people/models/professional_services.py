from django.db import models
from .base import BaseModel
from .person import Person


class ProfessionalServices(BaseModel):
    class Meta:
        verbose_name_plural = "Serviços de profissional"
        verbose_name = "Serviço de profissional"

    professional = models.ForeignKey(Person,
                                     on_delete=models.PROTECT,
                                     verbose_name="Profissional")

    title = models.CharField(default="Sem título",
                             max_length=120,
                             verbose_name="Título")

    description = models.TextField(max_length=600,
                                   blank=True,
                                   null=True,
                                   verbose_name='Descrição')

    @property
    def professional_name(self):
        return self.professional.name

    def __str__(self):
        return self.professional.name + " (" + self.description[:10] + ")"
