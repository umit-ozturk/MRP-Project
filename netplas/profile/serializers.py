from rest_framework import serializers
from profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'surname', 'created_at', )
