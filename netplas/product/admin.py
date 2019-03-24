from django.contrib import admin
from product.models import Product, Raw


class ProductAdmin(admin.ModelAdmin):
    list_display = ('stock', 'name', 'quantity', 'created_at', )
    search_fields = ('stock', 'name',)


class RawAdmin(admin.ModelAdmin):
    list_display = ('stock', 'name', 'quantity', 'created_at', )
    search_fields = ('stock', 'name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Raw, RawAdmin)
