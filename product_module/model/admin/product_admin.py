from django.contrib import admin
from django.contrib.admin import register
from django.utils.crypto import get_random_string
from django.utils.html import format_html

from helper_utils.jalalidate import format_jalali_dates_2
from product_module.model import Product, ProductFeature, ProductCategory
from product_module.model.forms import ProductColorAdminForm, ProductFeatureAdminForm
from product_module.model.product_color import ProductColor
from product_module.model.product_gallery import ProductGallery


def generateShortKey():
    rnd_code = get_random_string(length=7)
    while Product.objects.filter(short_key__exact=rnd_code).exists():
        rnd_code = get_random_string(length=7)
    return rnd_code


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    form = ProductColorAdminForm
    extra = 0
    min_num = 1
    validate_min = True


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    form = ProductFeatureAdminForm
    extra = 0
    min_num = 1
    validate_min = True


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 0
    min_num = 1
    readonly_fields = ['image_tag']
    fields = ['image_tag', 'image', 'title']
    validate_min = True


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))

    image_tag.short_description = 'تصویر محصول'

    # region jalali_date_format
    def persian_created_at(self, obj):
        return format_jalali_dates_2(obj.created_at)

    persian_created_at.short_description = 'تاریخ ثبت'

    def persian_updated_at(self, obj):
        return format_jalali_dates_2(obj.updated_at)

    persian_updated_at.short_description = 'آخرین بروزرسانی'
    # endregion

    list_display = ['title', 'price', 'image_tag', 'category', 'is_active', 'persian_created_at', 'persian_updated_at']
    list_filter = ['category', 'is_active', 'created_at', 'updated_at']
    list_editable = ['price', 'category', 'is_active']
    readonly_fields = ['short_key']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductGalleryInline, ProductColorInline, ProductFeatureInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.short_key = generateShortKey()
        obj.save()  # حتما باید محصول ذخیره شود تا pk بگیرد

    def save_related(self, request, form, formsets, change):
        # ابتدا related objects را ذخیره کن
        super().save_related(request, form, formsets, change)

        product = form.instance
        if not product.pk:
            # اگر به هر دلیلی محصول ذخیره نشده بود، کاری نکن
            return

        # حالا اولین رنگ را بیاب و قیمتش را برابر قیمت محصول قرار بده
        first_color = product.productcolor_set.order_by('created_at').first()
        if first_color and first_color.price != product.price:
            first_color.price = product.price
            first_color.save()

    # برای نمایش دسته بندی های فرزند برای انتخاب
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = ProductCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
