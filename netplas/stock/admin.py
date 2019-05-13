from django.contrib import admin
from stock.models import ProductStock, RawStock


class ProductStockAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj, request):
        css_class = {
            '1': 'success',
            '0': 'error',
        }
        status = 1 if obj.count > 0 else 0
        return {'class': css_class[str(status)], 'data': obj.name}

    list_display = ('id', 'name', 'created_at', 'count')
    search_fields = ('name',)


class RawStockAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj, request):
        css_class = {
            '1': 'success',
            '0': 'error',
        }
        status = 1 if obj.count > 0 else 0
        return {'class': css_class[str(status)], 'data': obj.name}
    list_display = ('id', 'name', 'created_at', 'count')
    search_fields = ('name',)


admin.site.register(ProductStock, ProductStockAdmin)
admin.site.register(RawStock, RawStockAdmin)
