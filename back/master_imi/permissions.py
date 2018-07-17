from django.contrib.auth.models import User
from rest_framework import permissions

from parcours_imi.models import UserParcours


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user

        if isinstance(obj, UserParcours):
            return obj.user == request.user

        return False
