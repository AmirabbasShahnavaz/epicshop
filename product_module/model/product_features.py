from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import BaseInlineFormSet

from product_module.model.feature import Feature
from product_module.model.product import Product


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,related_name='features', verbose_name="محصول")
    feature = models.ForeignKey(Feature,null=True,blank=False, on_delete=models.DO_NOTHING, verbose_name='نام ویژگی')
    feature_value = models.CharField(max_length=255, verbose_name="مقدار ویژگی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def __str__(self):
        return f'ویژگی ({self.feature.name}) مقدار ({self.feature_value})'

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی محصولات"
