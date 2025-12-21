from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'درحال بررسی'
    PAID = 'PAID', 'پرداخت شده'
    CANCELED = 'CANCELED' , 'لفو شده'
    FAILED = "FAILED" , "ناموفق"