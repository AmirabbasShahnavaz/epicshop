from django.contrib import admin
from django.utils.html import format_html

from web_module.model import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))

    image_tag.short_description = 'تصویر بنر'

    def url_tag(self, obj):
        return format_html('<a href="{}">رفتن به لینک</a>'.format(obj.url))

    url_tag.short_description = 'لینک بنر'

    list_display = ['title', 'type', 'image_tag','url_tag', 'is_active']
    list_filter = ['title','url', 'type', 'is_active']
    search_fields = ['title']