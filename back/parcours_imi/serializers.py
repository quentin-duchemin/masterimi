from django.contrib.auth.models import User
from rest_framework import serializers

from parcours_imi.models import Course, Master, UserParcours, UserCourseChoice


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class UserCourseChoiceSerializer(serializers.ModelSerializer):
    main_courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    option_courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    class Meta:
        model = UserCourseChoice
        fields = '__all__'

class UserParcoursSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    course_choice = UserCourseChoiceSerializer()

    class Meta:
        model = UserParcours
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    parcours = UserParcoursSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password',)
        depth = 1

