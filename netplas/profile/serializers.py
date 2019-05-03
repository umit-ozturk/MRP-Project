from django.template.defaultfilters import date as _date
from rest_framework import serializers
from profile.models import FirmPersonel


class UserProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = FirmPersonel
        fields = ('id', 'type', 'email', 'name', 'surname', 'created_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")
