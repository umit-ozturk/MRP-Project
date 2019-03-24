from django.contrib import admin
from stock.models import ProductStock, RawStock


class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', )
    search_fields = ('name',)


class RawStockAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', )
    search_fields = ('name',)


admin.site.register(ProductStock, ProductStockAdmin)
admin.site.register(RawStock, RawStockAdmin)
