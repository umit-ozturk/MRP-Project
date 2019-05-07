from django.contrib import admin
from product.models import Product, Raw, RawForProduction


class RawForProdAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj, request):
        css_class = {
            '0': 'success',
            '1': 'error'
        }
        status = 0 if obj.raw.stock.count > 0 else 1
        return {'class': css_class[str(status)]}          
    
    list_display = ('product', 'raw', 'quantity_for_prod', 'created_at', )


class ProductAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj, request):
        css_class = {
            '0': 'success',
            '1': 'error'
        }
        status = 0 if obj.stock.count > 0 else 1
        return {'class': css_class[str(status)]}  

    list_display = ('stock', 'name', 'created_at', )
    search_fields = ('stock', 'name',)


class RawAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj, request):
        css_class = {
            '0': 'success',
            '1': 'error'
        }
        status = 0 if obj.stock.count > 0 else 1
        return {'class': css_class[str(status)]}  
        
    list_display = ('stock', 'name', 'created_at', )
    search_fields = ('stock', 'name',)


admin.site.register(RawForProduction, RawForProdAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Raw, RawAdmin)
