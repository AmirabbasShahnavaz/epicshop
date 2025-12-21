from django.db import models

from order_module.model.order import Order
from product_module.model import Product
from product_module.model.product_color import ProductColor


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders", verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="products", verbose_name="محصول")
    product_color = models.ForeignKey(ProductColor, on_delete=models.DO_NOTHING, related_name="products", verbose_name="رنگ محصول")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت محصول")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="تعداد خرید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def get_total_price(self):
        return self.quantity * self.product_color.price