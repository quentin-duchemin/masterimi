from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from master_imi.permissions import IsOwner
from parcours_imi.models import Course, Master
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer,
    UserCourseChoiceSerializer, UserParcoursSerializer, UserSerializer,
)
from parcours_imi.tasks import send_validation_email


class CourseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class MasterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


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

    @action(methods=['GET'], detail=True)
    def parcours(self, request, *args, **kwargs):
        user = self.get_object()

        try:
            serialization_data = dict(instance=user.parcours)
        except User.parcours.RelatedObjectDoesNotExist:
            raise NotFound()

        serializer = UserParcoursSerializer(**serialization_data)

        return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def parcours_courses(self, request, *args, **kwargs):
        user = self.get_object()

        try:
            parcours = user.parcours
        except User.parcours.RelatedObjectDoesNotExist:
            raise NotFound()

        if parcours.course_choice and parcours.course_choice.submitted:
            raise PermissionDenied()

        serializer = UserCourseChoiceSerializer(instance=parcours.course_choice, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_validation_email.delay(serializer.data['id'])

        return Response(serializer.data)


