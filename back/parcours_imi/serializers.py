from django.contrib.auth.models import User
from rest_framework import serializers

from messaging.models import Conversation
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
    courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    coursesOption2 = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = UserParcours
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    parcours = UserParcoursSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password',)
        depth = 1

