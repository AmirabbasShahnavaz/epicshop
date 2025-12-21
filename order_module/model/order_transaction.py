from django.db import models

from order_module.model.choices import OrderStatus


class OrderTransaction(models.Model):
    order = models.ForeignKey('order_module.Order', on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='transactions')
    authority = models.CharField(max_length=255, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING,
                              verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    payment_gateway = models.CharField(max_length=50, default='ZarinPal')

    card_hash = models.CharField(max_length=500, default='')
    card_pan = models.CharField(max_length=500, default='')
    message = models.CharField(max_length=1000, default='')
    code = models.CharField(max_length=50, default='')
    ref_id = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"x{self.pk} {self.status}"
