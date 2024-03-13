from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from rest_framework.reverse import reverse

from .models import Product, Collection


# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    ordering = ['-unit_price']
    list_display_links = ['title', 'unit_price']
    search_fields = ['collections']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['id', 'title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection: Collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
        })
        )
        return format_html('<a href="{}">{} Products</a>', url, collection.products.count())

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )