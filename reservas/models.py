""" Modelos de entidades para reserva de salas """
from django.db import models

from users.models import Professor

# Create your models here.


class SalaModel(models.Model):
    """Modelo que representa a sala"""
    numero = models.IntegerField()
    bloco = models.IntegerField()
    capacidade = models.IntegerField()
    tipo = models.CharField(max_length=20)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f'Sala {self.numero}'

    class Meta:
        """Meta classe que define a nomenclatura no painel de administração"""
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


class ReservaModel(models.Model):
    """ Modelo que representa as Reservas """
    sala_numero = models.IntegerField()
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, related_name="reservas")

    def __str__(self):
        return f'Reserva - Sala[{self.sala_numero}] - [{self.hora_inicio}]'

    class Meta:
        """Meta classe que define a nomenclatura no painel de administração"""
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
