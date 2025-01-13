""" Módulo de ViewSets do app Reservas """
import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from reservas.api.serializers import BuscarSalaSerializer, ReservaSerializer, SalaSerializer
from reservas.models import ReservaModel, SalaModel
from reservas.services import SalaService
from users.api.permissions import IsProfessor
from users.models import Professor

logger = logging.getLogger("reservas")


class SalaViewSet(ModelViewSet):
    """ViewSet para manipulação das instâncias de Sala"""
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]
    queryset = SalaModel.objects.all()
    service = SalaService()

    def get_permissions(self):
        if self.action in ['create','update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = SalaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            nova_sala = self.service.create(data=serializer.validated_data)

            serializer_saida = SalaSerializer(nova_sala)
            logger.info("Sala Criada!")
            return Response(
                {"Info": "Sala criada!",
                    "data": serializer_saida.data},
                status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            logger.error("A sala já está cadastrada.")
            return Response(
                {"Info": "A sala já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response(
                {"Erro": "Comportamento Inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # from rest_framework.decorators import action
    # http://localhost:8000/salas/buscar/?sala=12
    @action(methods=['post'], detail=False, url_path="buscar")
    def buscar_sala(self, request):
        """Método para buscar salas"""
        serializer_input = BuscarSalaSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)

        id_sala = serializer_input.validated_data['sala']
        try:
            sala = SalaModel.objects.filter(id=id_sala).first()

            serializer = SalaSerializer(sala)
            return Response(
                {"Info": "Sala Encontrada!", "data": serializer.data},
                status=status.HTTP_200_OK)
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


class ReservaViewSet(ModelViewSet):
    """ ViewSet para manipulação de instâncias de Reserva """
    serializer_class = ReservaSerializer
    permission_classes = [AllowAny]
    queryset = ReservaModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ReservaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            sala_numero = serializer.validated_data['sala_numero']
            hora_inicio = serializer.validated_data['hora_inicio']
            hora_fim = serializer.validated_data['hora_fim']

            sala_existe = SalaModel.objects.filter(numero=sala_numero).exists()
            in_conflict = ReservaModel.objects.filter(
                sala_numero=sala_numero,
                hora_inicio__lt=hora_fim,
                hora_fim__gt=hora_inicio).exists()

            professor = Professor.objects.get(user=request.user)
            if sala_existe and not in_conflict:
                nova_reserva = ReservaModel.objects.create(
                    sala_numero=serializer.validated_data['sala_numero'],
                    hora_inicio=serializer.validated_data['hora_inicio'],
                    hora_fim=serializer.validated_data['hora_fim'],
                    professor=professor
                )

                serializer_saida = ReservaSerializer(nova_reserva)
                return Response(
                    {"Info": "Reserva cadastrada!",
                     "data": serializer_saida.data},
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"Info": "Falha ao tentar cadastrar reserva!"},
                    status=status.HTTP_409_CONFLICT)
        except Professor.DoesNotExist:
            return Response(
                {"Erro": "Apenas professores podem fazer reservas."},
                status=status.HTTP_403_FORBIDDEN)
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

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().list(request, args, kwargs)
        else:
            reservas = ReservaModel.objects.filter(professor__user=request.user)
            serializer = ReservaSerializer(reservas, many=True)
            return Response({"Reservas": serializer.data}, status=status.HTTP_200_OK)