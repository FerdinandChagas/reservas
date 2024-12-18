from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework import status

from reservas.models import ReservaModel, SalaModel
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import Professor

# Create your tests here.

class SalaTesteCase(TestCase):

    def setUp(self):
        self.nova_sala = SalaModel.objects.create(
            numero=3,
            bloco=1,
            capacidade=30,
            tipo="Aula",
            disponivel=True
        )
        # from rest_framework.authtoken.models import Token
        # from rest_framework.test import APIClient
        self.new_user = User.objects.create_user(username="admin",password="adminadmin")
        self.new_user.is_staff = True
        self.new_user.is_superuser = True
        self.new_user.save()
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_cadastrar_sala(self):
        url = "http://localhost:8000/salas/"
        data = {
            "numero": 2,
            "bloco": 2,
            "capacidade": 30,
            "tipo": "Aula",
            "disponivel": True
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SalaModel.objects.filter(numero=2,bloco=2).exists())

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_listar_salas(self):
        url = "http://localhost:8000/salas/"
        SalaModel.objects.create(
            numero=3,
            bloco=1,
            capacidade=30,
            tipo="Aula",
            disponivel=True
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['numero'], 3)

    def test_atualizar_salas(self):
        url = f"http://localhost:8000/salas/{self.nova_sala.id}/"
        data = {
            "numero": 19,
	        "bloco": 2,
	        "capacidade": 35,
	        "tipo": "Aula",
	        "disponivel": True
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_atualizar_parcialmente_salas(self):
        url = f"http://localhost:8000/salas/{self.nova_sala.id}/"
        data = {
	        "disponivel": False
        }
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.nova_sala.refresh_from_db()
        self.assertEqual(self.nova_sala.disponivel, False)
    
    def test_deletar_salas(self):
        url = f"http://localhost:8000/salas/{self.nova_sala.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SalaModel.objects.filter(id=self.nova_sala.id).exists())


class ReservaTesteCase(TestCase):

    def setUp(self):
        self.nova_sala = SalaModel.objects.create(
            numero=3,
            bloco=1,
            capacidade=30,
            tipo="Aula",
            disponivel=True
        )
        
        # from rest_framework.authtoken.models import Token
        # from rest_framework.test import APIClient
        self.new_user = User.objects.create_user(username="professor01",password="mudarsenha123")
        self.professor = Professor.objects.create(
            nome="Professor 01",
            matricula=5555,
            departamento="DEP",
            user=self.new_user
        )
        self.nova_reserva = ReservaModel.objects.create(
            sala_numero=3,
            hora_inicio="2024-12-12T08:00:00Z",
            hora_fim="2024-12-12T12:00:00Z",
            professor=self.professor
        )
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_cadastrar_reserva(self):
        url = "http://localhost:8000/reservas/"
        data = {
            "sala_numero": self.nova_sala.numero,
            "hora_inicio": "2025-01-12T08:00:00Z",
            "hora_fim": "2025-01-12T12:00:00Z"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ReservaModel.objects.filter(sala_numero=self.nova_sala.numero).exists())

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
    
    def test_listar_reservas(self):
        url = "http://localhost:8000/reservas/"
        ReservaModel.objects.create(
            sala_numero=self.nova_sala.numero,
            hora_inicio="2025-01-12T08:00:00Z",
            hora_fim="2025-01-12T12:00:00Z",
            professor=self.professor
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['sala_numero'], self.nova_sala.numero)

    def test_atualizar_reservas(self):
        url = f"http://localhost:8000/reservas/{self.nova_reserva.id}/"
        SalaModel.objects.create(
            numero=4,
            bloco=1,
            capacidade=30,
            tipo="Aula",
            disponivel=True
        )
        data = {
            "sala_numero": self.nova_sala.numero,
            "hora_inicio": "2025-02-12T08:00:00Z",
            "hora_fim": "2025-02-12T12:00:00Z"
        }
        response = self.client.put(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_atualizar_parcialmente_reservas(self):
        url = f"http://localhost:8000/reservas/{self.nova_reserva.id}/"
        data = {
	        "hora_fim": "2025-02-12T12:30:00Z"
        }
        response = self.client.patch(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_deletar_reservas(self):
        url = f"http://localhost:8000/reservas/{self.nova_reserva.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ReservaModel.objects.filter(id=self.nova_reserva.id).exists())