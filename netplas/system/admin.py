from django.contrib import admin
from system.models import Client, Supplier, ProductOrder, RawOrder, Budget, Product


class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'phone', 'created_at', )
    search_fields = ('name', 'surname', 'phone', )


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname', 'phone', 'created_at',)
    search_fields = ('name', 'surname', 'phone', )


class ProductOrderAdmin(admin.ModelAdmin):

    list_display = ('client', 'product', 'quantity',
                    'total', 'status', 'created_at', )
    search_fields = ('name', 'status', )


class RawOrderAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'raw', 'quantity',
                    'total', 'status', 'created_at',)
    search_fields = ('name', 'status', )


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('product_order', 'raw_order', 'user',
                    'total_income', 'total_outcome', 'created_at', 'updated_at',)
    search_fields = ('user', )


admin.site.register(Client, ClientAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(RawOrder, RawOrderAdmin)
admin.site.register(Budget, BudgetAdmin)
