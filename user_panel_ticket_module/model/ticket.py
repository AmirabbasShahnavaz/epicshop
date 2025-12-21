from django.db import models
from django.utils.crypto import get_random_string

from authentication_module.model import User
from user_panel_ticket_module.model.choices import TicketStatus, TicketPriorities, TicketSections


def generateTicketCode():
    rnd_code = get_random_string(length=7)
    while Ticket.objects.filter(ticket_code__exact=rnd_code).exists():
        rnd_code = get_random_string(length=7)
    return rnd_code


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    title = models.CharField(max_length=220, verbose_name='عنوان')
    status = models.CharField(max_length=100, choices=TicketStatus.choices, default=TicketStatus.Pending,
                              verbose_name='وضعیت')
    priority = models.CharField(max_length=100, choices=TicketPriorities.choices, verbose_name='الویت')
    section = models.CharField(max_length=100, choices=TicketSections.choices, verbose_name='بخش')
    ticket_code = models.CharField(max_length=10,default='', verbose_name='کد تیکت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def save(self, *args, **kwargs):
        if self._state.adding and not self.ticket_code:
            self.ticket_code = generateTicketCode()
        super().save(*args, **kwargs)
