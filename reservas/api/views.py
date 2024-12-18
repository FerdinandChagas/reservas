""" Módulo de ViewSets do app Reservas """
import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from reservas.api.serializers import ReservaSerializer, SalaSerializer
from reservas.models import ReservaModel, SalaModel
from users.api.permissions import IsProfessor
from users.models import Professor

logger = logging.getLogger("reservas")


class SalaViewSet(ModelViewSet):
    """ViewSet para manipulação das instâncias de Sala"""
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]
    queryset = SalaModel.objects.all()

    def get_permissions(self):
        if self.action in ['create','update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = SalaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            numero = serializer.validated_data['numero']
            bloco = serializer.validated_data['bloco']

            in_database = SalaModel.objects.filter(
                 numero=numero,
                 bloco=bloco).exists()

            if in_database:
                raise ValueError
            else:
                nova_sala = SalaModel.objects.create(
                    numero=serializer.validated_data['numero'],
                    bloco=serializer.validated_data['bloco'],
                    capacidade=serializer.validated_data['capacidade'],
                    tipo=serializer.validated_data['tipo'],
                    disponivel=serializer.validated_data['disponivel']
                )

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
    # http://localhost:8000/salas/buscar/?sala=12&bloco=2
    @action(methods=['get'], detail=False, url_path="buscar")
    def buscar_sala(self, request):
        """Método para buscar salas"""
        try:
            numero_sala = request.GET.get("sala")
            numero_bloco = request.GET.get("bloco")
            busca = SalaModel.objects.filter(
                numero=numero_sala, 
                bloco=numero_bloco)

            serializer = SalaSerializer(busca, many=True)
            return Response(
                {"Info": "Lista de Salas", "data": serializer.data},
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
    permission_classes = [IsAuthenticated]
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
