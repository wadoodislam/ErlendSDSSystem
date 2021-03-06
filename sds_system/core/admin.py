from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from .models import Product, Language, Wishlist, SDS_PDF, SDSHarvestSource, Manufacturer, SDSHarvestRun, SDSURLImport, \
    IgnoreDomain


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias')
    search_fields = ['name', 'alias']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'supplier', 'revision_date', 'matched', 'match', 'manufacturer_name', 'product_name', 'sds_revision_date')
    list_filter = ('matched',)
    search_fields = ['supplier', 'trade_name', ]

    def match(self, obj):
        if obj.matched:
            return format_html(f'<a href="{obj.sds_pdf.sds_link}" target="_blank">{obj.sds_pdf.sds_product_name}</a>')
        else:
            return format_html(f'<a href="/core/match/{obj.id}" target="_blank">Suggest</a>')

    def manufacturer_name(self, obj):
        return str(obj.sds_pdf.manufacturer) if obj.sds_pdf else None

    def product_name(self, obj):
        return str(obj.sds_pdf.sds_product_name) if obj.sds_pdf else None

    def sds_revision_date(self, obj):
        return str(obj.sds_pdf.sds_revision_date) if obj.sds_pdf else None


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
    list_display = ('name', 'primary', 'status', 'method', 'last_run_at', 'link_to_actions')
    list_filter = ('primary', 'status', 'type', 'method', )
    search_fields = ['name']

    def link_to_actions(self, obj):
        if obj.status == SDSHarvestSource.STATUS.DEVELOPED.value and obj.method == SDSHarvestSource.METHOD.SCRAPING.value:
            if ' ' in obj.id:
                return format_html('<a href="{}" target="_blank">Run</a>', reverse("core:run", args=[obj.id[:obj.id.index(' ')]]))
            return format_html('<a href="{}" target="_blank">Run</a>', reverse("core:run", args=[obj.id]))


class SDSHarvestRunAdmin(admin.ModelAdmin):
    list_display = ('sds_harvest_source', 'run_by', 'started_at', 'ended_at', 'no_of_revision_found', 'new_sds_found')
    list_filter = ('sds_harvest_source__name',)
    search_fields = ['sds_harvest_source__name']

    def new_sds_found(self, obj):
        return obj.no_of_new_sds_found

    def revision_found(self, obj):
        return obj.no_of_revision_found


class SDSURLImportAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_processed', 'is_downloaded', 'is_sds', 'is_duplicate', 'download_failed', 'pdf',)
    search_fields = ['domain']
    list_filter = ('is_processed', 'is_downloaded', 'is_sds', 'is_duplicate', 'download_failed',)

    def pdf(self, obj):
        if not obj.is_downloaded:
            return

        slug = slugify(obj.domain)
        return format_html(f'<a href="/media/sds/manual/{slug}/{slug}{obj.id}.pdf" target="_blank">PDF</a>')


class IgnoreDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'reason')
    search_fields = ['domain', 'reason']


admin.site.register(SDS_PDF, SDSPDFAdmin)
admin.site.register(IgnoreDomain, IgnoreDomainAdmin)
admin.site.register(SDSHarvestSource, SDSHarvestSourceAdmin)
admin.site.register(SDSHarvestRun, SDSHarvestRunAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(SDSURLImport, SDSURLImportAdmin)
admin.site.register(Language)
