from django.contrib import admin
from product.models import Product, Raw, RawForProduction


class RawForProdAdmin(admin.ModelAdmin):
    list_display = ('quantity_for_prod', 'created_at', )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('stock', 'name', 'created_at', )
    search_fields = ('stock', 'name',)


class RawAdmin(admin.ModelAdmin):
    list_display = ('stock', 'name', 'created_at', )
    search_fields = ('stock', 'name',)


admin.site.register(RawForProduction, RawForProdAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Raw, RawAdmin)
