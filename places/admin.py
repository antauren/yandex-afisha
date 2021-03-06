from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        if not obj.image:
            return 'изображение не загружено'
        return format_html('<img src="{}" height="{}"/>', obj.image.url, 200)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
