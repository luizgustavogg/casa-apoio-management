from django.db import models
from .base import BaseModel


class HouseConfiguration(BaseModel):
    """
    Configurações gerais da casa de apoio (singleton).
    Armazena a capacidade máxima de vagas.
    """
    
    class Meta:
        verbose_name = "Configuração da Casa"
        verbose_name_plural = "Configurações da Casa"
    
    max_capacity = models.PositiveIntegerField(
        default=20,
        verbose_name="Capacidade Máxima de Vagas",
        help_text="Número máximo de pessoas que podem estar hospedadas simultaneamente"
    )
    
    def __str__(self):
        return f"Configuração da Casa - Capacidade: {self.max_capacity} vagas"
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma instância existe (singleton)."""
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Impede a exclusão (singleton)."""
        pass
    
    @classmethod
    def get_config(cls):
        """Retorna a instância única de configuração."""
        config, created = cls.objects.get_or_create(pk=1)
        return config
    
    @staticmethod
    def get_current_occupancy():
        """
        Calcula a ocupação atual da casa com base em check-ins ativos.
        Retorna o número de check-ins ativos.
        """
        from .checkin import Checkin
        return Checkin.objects.filter(active=True).count()
    
    @staticmethod
    def get_available_vacancies():
        """
        Calcula o número de vagas disponíveis.
        Retorna: max_capacity - occupancy_atual
        """
        config = HouseConfiguration.get_config()
        current_occupancy = HouseConfiguration.get_current_occupancy()
        return max(0, config.max_capacity - current_occupancy)
    
    @staticmethod
    def is_at_full_capacity():
        """
        Verifica se a casa está com ocupação máxima.
        Retorna True se ocupação >= capacidade máxima.
        """
        return HouseConfiguration.get_available_vacancies() == 0
