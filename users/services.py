from django.contrib.auth.models import User, Group

from users.models import Professor

class ProfessorService:

    def create(self, data):
        novo_user = User.objects.create_user(
                username=data['login'],
                password=data['senha'],
            )
        grupo_professores, _ = Group.objects.get_or_create(name="Professores")
        novo_user.groups.add(grupo_professores)

        novo_professor = Professor.objects.create(
            nome=data['nome'],
            matricula=data['matricula'],
            departamento=data['departamento'],
            user=novo_user
        )
        return novo_professor