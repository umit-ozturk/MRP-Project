from rest_framework import serializers
from django.template.defaultfilters import date as _date
from product.models import Product, Raw, DamagedProduct, DamagedRaw
from stock.models import ProductStock, RawStock


class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductStock
        fields = ("id", "name",)


class RawStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = RawStock
        fields = ("id", "name",)


class ProductSerializer(serializers.ModelSerializer):
    stock = ProductStockSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", 'stock', 'name', 'quantity', 'created_at',)

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")


class RawSerializer(serializers.ModelSerializer):
    stock = RawStockSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Raw
        fields = ("id", 'stock', 'name', 'quantity', 'created_at',)

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")


class DamagedProductSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = DamagedProduct
        fields = ("id", 'product', 'created_at',)

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")


class DamagedRawSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = DamagedRaw
        fields = ("id", 'raw', 'created_at',)

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")
