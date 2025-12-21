from django.db import models

from authentication_module.model import User
from user_panel_ticket_module.model.ticket import Ticket


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages', verbose_name='تیکت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    message = models.TextField(max_length=800, verbose_name='متن پیام')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")