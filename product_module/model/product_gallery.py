from django.db import models
from django.utils.html import format_html

from product_module.model import Product


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name="محصول")
    title = models.CharField(max_length=150, verbose_name='عنوان عکس')
    image = models.ImageField(upload_to='images/product_galleries/', verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: cover;" />', self.image.url)
        return "تصویری موجود نیست"

    image_tag.short_description = "پیش‌نمایش"

    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری های محصول'