from rest_framework import serializers
from django.template.defaultfilters import date as _date
from system.models import Client, Supplier, RawOrder, ProductOrder, Budget
from product.serializers import RawSerializer, ProductSerializer
from profile.serializers import UserProfileSerializer


class ClientSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'email', 'name', 'surname',
                  'phone', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class SupplierSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ('id', 'email', 'name', 'surname',
                  'phone', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class RawOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=False, read_only=True)
    user = UserProfileSerializer(many=False, read_only=True)
    raw = RawSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = RawOrder
        fields = ('id', 'status', 'quantity', 'total',
                  'supplier', 'raw', 'created_at', 'updated_at', 'user')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class ProductOrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)
    product = ProductSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = ProductOrder
        fields = ('id', 'status', 'quantity', 'total',
                  'client', 'product', 'created_at', 'updated_at', 'user')

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class BudgetTotalSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'total', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")


class BudgetSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'total_income', 'total_outcome',
                  'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y - H:m")
