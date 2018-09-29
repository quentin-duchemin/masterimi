from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from master_imi.permissions import IsOwner
from parcours_imi.models import AttributeConstraint, Course, Master, OPTIONS_KEYS
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer,
    UserCourseChoiceSerializer, UserParcoursSerializer, UserSerializer,
)
from parcours_imi.validators import AttributeConstraintsValidator, TimeCollisionValidator
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
            if self.request.user is None:
                raise NotAuthenticated()

            return self.request.user
        else:
            return super().get_object()

    @action(methods=['GET'], detail=True)
    def parcours(self, request, *args, **kwargs):
        parcours = self._get_user_parcours()

        serializer = UserParcoursSerializer(instance=parcours)

        return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def parcours_option(self, request, *args, **kwargs):
        parcours = self._get_user_parcours()

        if parcours.option:
            raise PermissionDenied()

        option = request.data.get('option')
        if option not in OPTIONS_KEYS:
            raise ValidationError('Invalid option')

        parcours.option = option
        parcours.save()

        send_option_confirmation_email.delay(parcours.id)

        serializer = UserParcoursSerializer(instance=parcours)

        return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def parcours_courses(self, request, *args, **kwargs):
        parcours = self._get_user_parcours()

        if parcours.course_choice and parcours.course_choice.submitted:
            raise PermissionDenied()

        serializer = self._get_parcours_courses_serializer(parcours, request.data)

        is_submitted = serializer.validated_data['submitted']

        if is_submitted:
            parcours_validation_data = self._get_parcours_courses_rules_validation_data(parcours, serializer)

            errors = [
                item['message']
                for item in parcours_validation_data
                if item['type'] == 'error'
            ]
            if errors:
                raise ValidationError(errors)

        with transaction.atomic():
            course_choice = serializer.save()
            parcours.course_choice = course_choice
            parcours.save()

        if is_submitted:
            send_courses_validation_email.delay(parcours.id, parcours_validation_data)

        return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def parcours_courses_check(self, request, *args, **kwargs):
        parcours = self._get_user_parcours()

        serializer = self._get_parcours_courses_serializer(parcours, request.data)
        parcours_validation_data = self._get_parcours_courses_rules_validation_data(parcours, serializer)

        return Response(parcours_validation_data)

    def _get_user_parcours(self):
        user = self.get_object()

        try:
            parcours = user.parcours
        except User.parcours.RelatedObjectDoesNotExist:
            raise NotFound()

        return parcours

    def _get_parcours_courses_serializer(self, parcours, data):
        serializer = UserCourseChoiceSerializer(instance=parcours.course_choice, data=data, partial=False)
        serializer.is_valid(raise_exception=True)

        return serializer

    def _get_parcours_courses_rules_validation_data(self, parcours, serializer):
        attribute_constraints_validator = AttributeConstraintsValidator(
            constraints=parcours.master.attribute_constraints.all(),
            attributes_getter=lambda course: course.attributes,
        )
        attribute_constraints_validation_data = attribute_constraints_validator.validate(
            serializer.validated_data['main_courses']
        )

        time_collision_validation_data = TimeCollisionValidator().validate(
            serializer.validated_data['main_courses'] + serializer.validated_data['option_courses']
        )

        if parcours.option == '3A-M2-ECTS':
            option_validator = AttributeConstraintsValidator(
                constraints=[
                    AttributeConstraint.objects.get(pk='8ce0b5ea-7e1d-4d7a-b5e6-77c83ed0d4d9')
                ],
                attributes_getter=lambda course: course.attributes,
            )
            option_validation_data = option_validator.validate(
                serializer.validated_data['option_courses']
            )

            return attribute_constraints_validation_data + option_validation_data + time_collision_validation_data

        return attribute_constraints_validation_data + time_collision_validation_data
