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
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class SupplierSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ('id', 'email', 'name', 'surname',
                  'phone', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class RawOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(many=False, read_only=True)
    personal = UserProfileSerializer(many=False, read_only=True)
    raw = RawSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = RawOrder
        fields = ('id', 'status', 'quantity', 'total',
                  'supplier', 'raw', 'created_at', 'updated_at', 'personal')

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class ProductOrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True)
    product = ProductSerializer(many=False, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    personal = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = ProductOrder
        fields = ('id', 'status', 'quantity', 'total',
                  'client', 'product', 'created_at', 'updated_at', 'personal')

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class BudgetSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'total_income', 'total_outcome',
                  'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")
