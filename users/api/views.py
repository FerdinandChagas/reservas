import logging
from django.contrib.auth.models import User, Group
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from users.api.permissions import IsProfessor
from users.api.serializers import ProfessorCreateSerializer, ProfessorSerializer, UserProfileExampleSerializer

from users.models import Professor, UserProfileExample

logger = logging.getLogger("reservas")


class UserProfileExampleViewSet(ModelViewSet):
    """ViewSet de exemplo para manipulação de perfis de Usuários"""
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
    queryset = UserProfileExample.objects.all()
    http_method_names = ['get', 'put']


class ProfessorViewSet(ModelViewSet):
    """ViewSet para manipulação das entidades do tipo Professor"""
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Professor.objects.all()

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy']:
            return [IsProfessor()]
        elif self.action == 'list':
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = ProfessorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            novo_user = User.objects.create_user(
                username=serializer.validated_data['login'],
                password=serializer.validated_data['senha'],
            )
            grupo_professores = Group.objects.get(name="Professores")
            novo_user.groups.add(grupo_professores)

            novo_professor = Professor.objects.create(
                nome=serializer.validated_data['nome'],
                matricula=serializer.validated_data['matricula'],
                departamento=serializer.validated_data['departamento'],
                user=novo_user
            )

            serializer_saida = ProfessorSerializer(novo_professor)
            return Response(
                {"Info": "Cadastro realizado!",
                 "data": serializer_saida.data},
                status=status.HTTP_201_CREATED)
        except ValueError:
            logger.error("Entrada inválida.")
            return Response(
                {"Erro": "Dados inválidos!"},
                status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated:
            return Response(
                {"Erro": "Usuário não autenticado."},
                status=status.HTTP_401_UNAUTHORIZED)
