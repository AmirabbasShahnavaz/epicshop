from django.db import models

from authentication_module.model import User


class WalletStatus(models.TextChoices):
    Creditor = 'Creditor', 'برداشت'
    Deposit = 'Deposit', 'واریز'
    Pending = 'Pending','در حال بررسی'


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='کاربر')
    amount = models.DecimalField(max_digits=10, decimal_places=0,verbose_name='مبلغ')
    status = models.CharField(max_length=10, choices=WalletStatus.choices,
                              default=WalletStatus.Pending,
                              verbose_name='وضعیت')
    description = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
