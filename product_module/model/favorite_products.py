from django.db import models

from authentication_module.model import User
from product_module.model import Product


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, verbose_name='محصول')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = 'علاقه مندی محصول'
        verbose_name_plural = 'علاقه مندی محصولات'