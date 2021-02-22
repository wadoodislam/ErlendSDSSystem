from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Language, Wishlist, SDS_PDF, SDSHarvestSource, Manufacturer


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias')
    search_fields = ['name', 'alias']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'supplier', 'language', 'matched', 'match')
    list_filter = ('matched',)
    search_fields = ['supplier', 'trade_name', ]

    def match(self, obj):
        if obj.matched:
            return format_html(f'<a href="{obj.product.link}" target="_blank">{obj.product.sds_product_name}</a>')
        else:
            return format_html(f'<a href="/core/match/{obj.id}" target="_blank">Suggest</a>')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'sds_harvest_source', 'pdf')
    list_filter = ('sds_pdf__sds_harvest_source', 'sds_pdf__manufacturer',)
    search_fields = ['name', 'sds_pdf__name', 'sds_pdf__manufacturer__name',
                     'sds_pdf__sds_harvest_source__name', 'sds_pdf__sds_product_name',]

    def pdf(self, obj):
        return format_html(f'<a href="{obj.sds_pdf.sds_download_url}" target="_blank">PDF</a>')

    def manufacturer(self, obj):
        return str(obj.sds_pdf.manufacturer)

    def sds_harvest_source(self, obj):
        return str(obj.sds_pdf.sds_harvest_source)


class SDSPDFAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'sds_harvest_source', 'pdf', 'sds_hazards_codes',)
    list_filter = ('sds_harvest_source', 'manufacturer',)
    search_fields = ['name', 'manufacturer__name', 'sds_harvest_source__name', 'sds_product_name',]

    def pdf(self, obj):
        return format_html(f'<a href="{obj.sds_download_url}" target="_blank">PDF</a>')


class SDSHarvestSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary', 'status', 'type', 'method',)
    list_filter = ('primary', 'status', 'type', 'method',)
    search_fields = ['name']


admin.site.register(SDS_PDF, SDSPDFAdmin)
admin.site.register(SDSHarvestSource, SDSHarvestSourceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Language)
