from datetime import datetime

from django.db import models

from product_module.model import Product


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    name = models.CharField(max_length=100, verbose_name='نام رنگ')
    color_code = models.CharField(max_length=7, verbose_name='رنگ')
    price = models.DecimalField(null=True, blank=False, decimal_places=0, max_digits=9, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(null=True, blank=False, verbose_name='تعداد')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.color_code})"

    class Meta:
        verbose_name = "رنگ محصول"
        verbose_name_plural = "رنگ های محصول"
