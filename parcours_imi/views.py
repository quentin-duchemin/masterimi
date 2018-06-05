from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated

from parcours_imi.models import Course, Master, UserParcours
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer, UserParcoursSerializer, UserSerializer,
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class MasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


class UserParcoursViewSet(viewsets.ModelViewSet):
    serializer_class = UserParcoursSerializer
    queryset = UserParcours.objects.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.kwargs['pk']
        if pk == 'me':
            if self.request.auth is None:
                raise NotAuthenticated()

            return self.request.user
        else:
            return super().get_object()
