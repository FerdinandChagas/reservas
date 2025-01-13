from rest_framework import serializers

from reservas.models import ReservaModel, SalaModel

class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalaModel
        fields = "__all__"

class BuscarSalaSerializer(serializers.Serializer):
    sala = serializers.IntegerField()

class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReservaModel
        fields = ['sala_numero', 'hora_inicio', 'hora_fim', 'professor']
