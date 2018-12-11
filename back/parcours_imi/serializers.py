from django.contrib.auth.models import User
from rest_framework import serializers

from parcours_imi.models import Course, Master, Option, UserParcours, UserCourseChoice


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    available_options = OptionSerializer(many=True, read_only=True)

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
    option = OptionSerializer()

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

