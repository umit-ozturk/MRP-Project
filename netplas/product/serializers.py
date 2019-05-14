from rest_framework import serializers
from django.template.defaultfilters import date as _date
from product.models import Product, Raw, RawForProduction, ProductAttr
from stock.serializers import ProductStockSerializer, RawStockSerializer


class RawUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raw
        fields = ('stock', 'name', 'amount', 'unit_price')


class RawSerializer(serializers.ModelSerializer):
    stock = RawStockSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Raw
        fields = ("id", 'stock', 'name', 'amount',
                  'created_at', 'updated_at', 'unit_price')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class RawForProdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawForProduction
        fields = ('raw', 'product', 'quantity_for_prod')


class RawForProdSerializer(serializers.ModelSerializer):
    raw = RawStockSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    product = ProductStockSerializer(many=False, read_only=True)

    class Meta:
        model = RawForProduction
        fields = ("id", 'raw', 'quantity_for_prod',
                  'created_at', 'updated_at', 'product')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class ExcludeProductRawForProdSerializer(serializers.ModelSerializer):
    raw = RawStockSerializer(many=False, read_only=True)

    class Meta:
        model = RawForProduction
        fields = ("id", 'raw', 'quantity_for_prod', )


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('stock', 'name', 'amount', 'unit_price')


class ProductSerializer(serializers.ModelSerializer):
    stock = ProductStockSerializer(many=False, read_only=True)
    raw_for_prod = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    product_attr = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", 'stock', 'raw_for_prod', 'name',
                  'amount', 'unit_price', 'created_at', 'updated_at', 'product_attr')

    def get_raw_for_prod(self, obj):
        raw_recipe = RawForProduction.objects.filter(product__name=obj.name)
        return ExcludeProductRawForProdSerializer(raw_recipe, many=True).data

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_product_attr(self, obj):
        data = {}
        for item in obj.attr.all().values_list('name', 'value', 'id'):
            data.update(
                {
                    str(item[2]): {
                        item[0]: item[1]
                    }
                }
            )
        return data


class ProductAttrSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttr
        fields = ('product', 'name', 'value')
