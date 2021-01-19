from django.contrib import admin
from django.utils.html import format_html

from .models import Provider, Product, Language, Wishlist


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary')
    search_fields = ['name',]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'trade_name', 'language', 'matched',)
    list_filter = ('matched',)
    search_fields = ['supplier', 'trade_name', ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sds_product_name', 'sds_manufacture_name', 'provider', 'pdf', 'sds_hazards_codes',)
    list_filter = ('provider',)
    search_fields = ['sds_manufacture_name', 'provider__name', 'sds_product_name']

    def pdf(self, obj):
        return format_html(f'<a href="{obj.link}" target="_blank">PDF</a>')


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Language)
