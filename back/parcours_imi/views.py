from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from parcours_imi.models import Course, Master, UserParcours
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer, UserParcoursSerializer, UserSerializer,
)


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


class CourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)


class MasterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = (IsAuthenticated,)


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        pk = self.kwargs['pk']
        if pk == 'me':
            if self.request.auth is None:
                raise NotAuthenticated()

            return self.request.user
        else:
            return super().get_object()

    @action(methods=['GET', 'PUT'], detail=True)
    def parcours(self, request, *args, **kwargs):
        user = self.get_object()

        if request.method.upper() == 'GET':
            try:
                serialization_data = dict(instance=user.parcours)
            except User.parcours.RelatedObjectDoesNotExist:
                serialization_data = dict()

            serializer = UserParcoursSerializer(**serialization_data)

            return Response(serializer.data)

        if request.method.upper() == 'PUT':
            try:
                parcours = user.parcours
            except User.parcours.RelatedObjectDoesNotExist:
                parcours = None

            if parcours and parcours.submitted:
                raise PermissionDenied()

            request.data['user'] = request.user.id
            serializer = UserParcoursSerializer(instance=parcours, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        raise NotImplementedError


