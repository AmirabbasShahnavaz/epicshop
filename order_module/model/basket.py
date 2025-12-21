from django.db import models

from authentication_module.model import User
from product_module.model import Product
from product_module.model.product_color import ProductColor


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    guest_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, verbose_name="رنگ محصول")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="تعداد خرید")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def get_total_price(self):
        return self.quantity * self.product_color.price

    def __str__(self):
        if self.user:
            return f'{self.product} in basket {self.user}'
        return f'{self.product} in basket {self.guest_id}'
