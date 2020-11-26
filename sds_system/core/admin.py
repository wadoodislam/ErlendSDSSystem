from django.contrib import admin

from .models import Provider, Product, Language


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sds_pdf_product_name', 'sds_pdf_manufacture_name', 'sds_pdf_Hazards_identification', 'provider')
    list_filter = ('provider',)
    search_fields = ['sds_pdf_manufacture_name', 'provider__name', 'sds_pdf_product_name']


admin.site.register(Provider)
admin.site.register(Product, ProductAdmin)
admin.site.register(Language)
