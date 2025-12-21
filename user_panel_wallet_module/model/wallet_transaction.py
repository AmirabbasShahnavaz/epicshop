from django.db import models

from user_panel_wallet_module.model import Wallet


class WalletTransactionStatus(models.TextChoices):
    PENDING = 'PENDING', 'درحال بررسی'
    PAID = 'PAID', 'پرداخت شده'
    FAILED = "FAILED", "ناموفق"


class WalletTransaction(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name='کیف پول')
    authority = models.CharField(max_length=255, default='')
    payment_gateway = models.CharField(max_length=50, default='ZarinPal')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=WalletTransactionStatus.choices,
                              default=WalletTransactionStatus.PENDING,
                              verbose_name='وضعیت')
    card_hash = models.CharField(max_length=500, default='')
    card_pan = models.CharField(max_length=500, default='')
    message = models.CharField(max_length=1000, default='')
    code = models.CharField(max_length=50, default='')
    ref_id = models.CharField(max_length=255, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
