from rest_framework import serializers
from django.template.defaultfilters import date as _date
from stock.models import ProductStock, RawStock


class ProductStockSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = ProductStock
        fields = ('id', 'name', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class RawStockSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = RawStock
        fields = ('id', 'name', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")
