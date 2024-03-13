from django.contrib import admin

from changes.models import Article


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'character_count')
    list_filter = ('published',)
    show_facets = admin.ShowFacets.ALWAYS
