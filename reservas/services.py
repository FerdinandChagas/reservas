
from reservas.models import SalaModel


class SalaService:

    def create(self, data):
        numero = data['numero']
        bloco = data['bloco']

        in_database = SalaModel.objects.filter(
                numero=numero,
                bloco=bloco).exists()
        
        if in_database:
            raise ValueError
        else:
            nova_sala = SalaModel.objects.create(
                numero=data['numero'],
                bloco=data['bloco'],
                capacidade=data['capacidade'],
                tipo=data['tipo'],
                disponivel=data['disponivel']
            )
            return nova_sala

    