from django.contrib import admin
from django.contrib.admin import register

from product_module.model.feature import Feature


@register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']