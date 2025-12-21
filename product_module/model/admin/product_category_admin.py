from django.contrib import admin
from django.contrib.admin import register
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

from product_module.model import ProductCategory


@register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            thumb = get_thumbnail(
                obj.image,
                '100x100',
                crop='center',
                quality=60
            )
            return format_html(
                '<img src="{}" width="100" height="100" />',
                thumb.url
            )
        return '—'

    image_tag.short_description = 'تصویر دسته'

    list_display = ['title', 'parent','image_tag', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title']
    prepopulated_fields = {'url_title': ('title',)}

    # این فانکشن برای پایینی بدرد میخوره
    def get_descendants(self, category):
        """زیرشاخه‌های بازگشتی"""
        descendants = []
        children = ProductCategory.objects.filter(parent=category)
        for child in children:
            descendants.append(child.id)
            descendants.extend(self.get_descendants(child))
        return descendants

    # این برای اینکه هم داخل ویرایش دسته بندی والد خودش رو داخل لیست دسته بندی های والد نباره و موقع اضافه شدن فقط اونایی که دسته بندی والد هستن رو میاره برای انتخاب
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            object_id = request.resolver_match.kwargs.get("object_id")

            if object_id:  # حالت ویرایش
                current_category = ProductCategory.objects.get(pk=object_id)
                exclude_ids = [current_category.id] + self.get_descendants(current_category)
                kwargs["queryset"] = ProductCategory.objects.exclude(id__in=exclude_ids, parent__isnull=True)
            else:  # حالت افزودن
                kwargs["queryset"] = ProductCategory.objects.filter(parent__isnull=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
