from django.db import models
from .base import BaseModel
from .checkin import Checkin


class Checkout(BaseModel):
    class Meta:
        verbose_name_plural = "Check-out's"
        verbose_name = "Check-out"

    checkin = models.OneToOneField(Checkin, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Fechado em")

    def __str__(self):
        return self.checkin.person.name + " " + self.created_at.strftime(
            "%d/%m/%Y")
