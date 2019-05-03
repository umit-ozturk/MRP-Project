from rest_framework import serializers
from django.template.defaultfilters import date as _date
from system.models import Client, Supplier, RawOrder, ProductOrder, Budget


class ClientSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'email', 'name', 'surname', 'phone', 'created_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")


class SupplierSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ('id', 'email', 'name', 'surname', 'phone', 'created_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")


class RawOrderSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = RawOrder
        fields = ('id', 'name', 'status', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class ProductOrderSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = ProductOrder
        fields = ('id', 'name', 'status', 'created_at', 'updated_at', )

    def get_created_at(self, obj):
        return _date(obj.created_at, "d F, Y")

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")


class BudgetSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ('id', 'total_income', 'total_outcome', 'updated_at', )

    def get_updated_at(self, obj):
        return _date(obj.updated_at, "d F, Y")
