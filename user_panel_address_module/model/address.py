from django.db import models

from authentication_module.model import User
from user_panel_address_module.model.state import State


class Address(models.Model):

    label = models.CharField(max_length=150, verbose_name="برچسب آدرس")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    province = models.ForeignKey(State, on_delete=models.CASCADE, related_name='user_provinces')

    city = models.ForeignKey(State, on_delete=models.CASCADE, related_name='user_cities')

    plate_number = models.IntegerField(verbose_name="پلاک")

    home_unit = models.IntegerField(null=True, blank=True, verbose_name="واحد")

    phone_number = models.CharField(max_length=15, verbose_name="تلفن ثابت")

    street_or_neighborhood = models.CharField(max_length=300, verbose_name="خیابان یا محله")

    full_address = models.CharField(max_length=800, verbose_name="آدرس کامل")

    description = models.CharField(max_length=500, verbose_name="توضیحات آدرس")

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
