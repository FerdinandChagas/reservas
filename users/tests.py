from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Create your tests here.


class UserTestCase(TestCase):
    """ Test Case example """

    def setUp(self) -> None:
        self.new_user = User.objects.create_user(username="professor01",password="mudarsenha123")
        professor_group, _ = Group.objects.get_or_create(name="Professor")
        self.new_user.groups.add(professor_group)
        self.new_user.save()
        self.token, _ = Token.objects.get_or_create(user=self.new_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_cadastrar_professor(self):
        url = "http://localhost:8000/professores/"
        data = {
            "nome": "Professor Teste",
            "matricula": 7777,
            "departamento": "DC",
            "login": "professor_teste",
            "senha": "mudarsenha123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)