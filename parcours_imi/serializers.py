from django.contrib.auth.models import User
from rest_framework import serializers

from parcours_imi.models import Course, Master, UserProfile, Option


class MasterSerializer(serializers.ModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='userprofile-detail'
    )
    courses = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='courses-detail'
    )

    class Meta:
        model = Master
        fields = ('id', 'name', 'website', 'troisa_possible', 'profiles', 'courses')


class CourseSerializer(serializers.ModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='userprofile-detail'
    )

    class Meta:
        model = Course
        fields = '__all__'
        extra_fields = ['profiles']


class OptionSerializer(serializers.ModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='userprofile-detail'
    )

    class Meta:
        model = Option
        fields = '__all__'
        extra_fields = ['profiles']


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'option', 'master'
        )

    def update(self, instance, validated_data):
        # user = User.objects.get(pk = instance.user.pk);
        user = instance.user
        user.email = validated_data.get('user.email', user.email)
        user.first_name = validated_data.get('user.first_name', user.first_name)
        user.last_name = validated_data.get('user.last_name', user.last_name)
        user.username = validated_data.get('user.username', user.username)
        user.save()

        instance.save()

        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        depth = 1

