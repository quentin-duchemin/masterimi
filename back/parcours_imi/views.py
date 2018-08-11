from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from master_imi.permissions import IsOwner
from parcours_imi.models import Course, Master, OPTIONS_KEYS
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer,
    UserCourseChoiceSerializer, UserParcoursSerializer, UserSerializer,
)
from parcours_imi.tasks import send_option_confirmation_email, send_courses_validation_email


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
    def parcours_option(self, request, *args, **kwargs):
        user = self.get_object()

        try:
            parcours = user.parcours
        except User.parcours.RelatedObjectDoesNotExist:
            raise NotFound()

        if parcours.option:
            raise PermissionDenied()

        option = request.data.get('option')
        if option not in OPTIONS_KEYS:
            raise ValidationError('Invalid option')

        parcours.option = option
        parcours.save()

        send_option_confirmation_email.delay(user.id)

        serializer = UserParcoursSerializer(instance=parcours)

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

        with transaction.atomic():
            course_choice = serializer.save()
            parcours.course_choice = course_choice
            parcours.save()

        send_courses_validation_email.delay(user.id)

        return Response(serializer.data)


