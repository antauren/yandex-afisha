from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        html = '<img src="{url}" height="{height}"/>'.format(url=obj.image.url,
                                                             height=200,
                                                             )
        return format_html('{}', mark_safe(html))


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
