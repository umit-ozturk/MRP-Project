from rest_framework import serializers
from system.models import Client, Supplier, RawOrder, ProductOrder, Budget


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'email', 'name', 'surname', 'phone', 'created_at', )


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('id', 'email', 'name', 'surname', 'phone', 'created_at', )


class RawOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = RawOrder
        fields = ('id', 'name', 'status', 'created_at', 'updated_at', )


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrder
        fields = ('id', 'name', 'status', 'created_at', 'updated_at', )


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('id', 'total', 'updated_at', )
