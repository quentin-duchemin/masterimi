from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from parcours_imi.models import Course, Master, Option, UserProfile
from parcours_imi.serializers import (
    CourseSerializer, MasterSerializer, OptionSerializer, UserProfileSerializer,
    UserSerializer,
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class MasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
