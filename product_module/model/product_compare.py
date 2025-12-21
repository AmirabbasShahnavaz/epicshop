from django.db import models

from authentication_module.model import User
from product_module.model import Product


class ProductCompare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    guest_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")