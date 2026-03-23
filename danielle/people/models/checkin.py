from django.db import models
from .base import BaseModel
from .person import Person


class Checkin(BaseModel):
    class Meta:
        verbose_name_plural = "Check-in's"
        verbose_name = "Check-in"
        ordering = ['-created_at']

    person = models.ForeignKey(Person,
                               verbose_name='Pessoa',
                               related_name='main_person',
                               on_delete=models.PROTECT)

    REASON_CHOICES = [('patient', 'Paciente'), ('companion', 'Acompanhante'),
                      ('professional', 'Profissional'),
                      ('voluntary', 'Voluntário'), ('visitor', 'Visitantes'),
                      ('other', 'Outros')]

    reason = models.CharField(max_length=12,
                              choices=REASON_CHOICES,
                              verbose_name='Tipo de check-in')

    companion = models.ForeignKey(Person,
                                  blank=True,
                                  null=True,
                                  related_name='companion',
                                  verbose_name='Acompanhante',
                                  on_delete=models.PROTECT)

    chemotherapy = models.BooleanField(default=False,
                                       verbose_name='Quimioterapia')
    radiotherapy = models.BooleanField(default=False,
                                       verbose_name='Radioterapia')
    surgery = models.BooleanField(default=False, verbose_name='Cirurgia')
    exams = models.BooleanField(default=False, verbose_name='Exames')
    appointment = models.BooleanField(default=False, verbose_name='Consultas')
    other = models.BooleanField(default=False, verbose_name='Outros')

    ca_number = models.CharField(max_length=20,
                                 blank=True,
                                 null=True,
                                 verbose_name='Número C.A.')

    social_vacancy = models.BooleanField(blank=True,
                                         null=True,
                                         verbose_name="Vaga Social?")

    observation = models.TextField(max_length=600,
                                   blank=True,
                                   null=True,
                                   verbose_name='Observação')

    active = models.BooleanField(default=True,
                                 blank=True,
                                 verbose_name="Ativo")

    @property
    def companion_name(self):
        if self.companion:
            return self.companion.name

    @property
    def person_name(self):
        return self.person.name

    def __str__(self):
        return self.person.name + " " + self.created_at.strftime(
            "(Entrada em %d/%m/%Y %H:%M)")


class PatientCompanionCheckin(BaseModel):
    patient = models.ForeignKey(Person,
                                verbose_name='Paciente',
                                related_name='patient_checkin',
                                on_delete=models.PROTECT)
    companion = models.ForeignKey(Person,
                                  verbose_name="Acompanhante",
                                  related_name='companion_checkin',
                                  on_delete=models.PROTECT)
