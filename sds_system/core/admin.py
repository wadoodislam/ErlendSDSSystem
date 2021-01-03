from django.contrib import admin

from .models import Provider, Product, Language, SDS


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sds_product_name', 'sds_manufacture_name', 'sds_hazards_codes', 'provider')
    list_filter = ('provider',)
    search_fields = ['sds_manufacture_name', 'provider__name', 'sds_product_name']


admin.site.register(Provider)
admin.site.register(SDS)
admin.site.register(Product, ProductAdmin)
admin.site.register(Language)
