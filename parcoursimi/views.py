from parcoursimi.models import Courses, Master, Option, UserProfile
from parcoursimi.serializers import CoursesSerializer, MasterSerializer,OptionSerializer, UserProfileSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status



class CoursesList(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer

class MasterList(generics.ListCreateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

class OptionList(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MasterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

class CoursesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
    

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'userprofile': reverse('userprofile-list', request=request, format=format),
        'courses': reverse('courses-list', request=request, format=format),
        'option': reverse('option-list', request=request, format=format),
        'master': reverse('master-list', request=request, format=format)
    })

    
    