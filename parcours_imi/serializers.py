from django.contrib.auth.models import User
from rest_framework import serializers

from parcours_imi.models import Course, Master, UserParcours


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class UserParcoursSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)

    courses = CourseSerializer(many=True, read_only=True)
    coursesOption2 = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = UserParcours
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    parcours = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        exclude = ('password',)
        depth = 1

