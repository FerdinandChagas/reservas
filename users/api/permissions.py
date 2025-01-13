from rest_framework import permissions

from reservas.models import ReservaModel

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Professores").exists()
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, ReservaModel):
            return obj.professor.user == request.user
        return super().has_object_permission(request, view, obj)
    