from rest_framework import serializers
from django.template.defaultfilters import date as _date
from product.models import Product, Raw, DamagedProduct, DamagedRaw, RawForProduction
from stock.serializers import ProductStockSerializer, RawStockSerializer


class RawSerializer(serializers.ModelSerializer):
    stock = RawStockSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Raw
        fields = ("id", 'stock', 'name', 'amount', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class RawForProdSerializer(serializers.ModelSerializer):
    raw = RawStockSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = RawForProduction
        fields = ("id", 'raw', 'quantity_for_prod', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class ProductSerializer(serializers.ModelSerializer):
    stock = ProductStockSerializer(many=False, read_only=True)
    raw_for_prod = RawForProdSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", 'stock', 'raw_for_prod', 'name', 'amount', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class DamagedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = DamagedProduct
        fields = ("id", 'product', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class DamagedRawSerializer(serializers.ModelSerializer):
    raw = RawSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = DamagedRaw
        fields = ("id", 'raw', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")
