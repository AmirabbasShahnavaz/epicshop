from django.contrib import admin
from django.contrib.admin import register

from helper_utils.jalalidate import format_jalali_dates_2
from user_panel_wallet_module.model import Wallet


@register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    # region jalali_date_format
    def persian_created_at(self, obj):
        return format_jalali_dates_2(obj.created_at)

    persian_created_at.short_description = 'تاریخ ثبت'

    def persian_updated_at(self, obj):
        return format_jalali_dates_2(obj.updated_at)

    persian_updated_at.short_description = 'آخرین بروزرسانی'
    # endregion

    list_display = ['description', 'user', 'amount', 'status', 'persian_created_at', 'persian_updated_at']
    list_filter = ['user', 'status', 'created_at', 'updated_at']
