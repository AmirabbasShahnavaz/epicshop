from django.db import models

from authentication_module.model import User
from .order_transaction import OrderTransaction
from order_module.model.choices import OrderStatus
from user_panel_address_module.model import Address


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='کاربر')
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, verbose_name='آدرس')
    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    amount = models.DecimalField(max_digits=9,decimal_places=0,verbose_name="قیمت قابل پرداخت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def get_order_transaction(self):
        transaction = OrderTransaction.objects.filter(order_id=self.id).exclude(status=OrderStatus.PENDING).first()
        if transaction:
            return transaction
        return '-'

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"