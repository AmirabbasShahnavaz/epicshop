from django.contrib import admin
from django.utils.html import format_html

from helper_utils.jalalidate import format_jalali_dates_2
from user_panel_ticket_module.model import TicketMessage, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    def view_chat_link(self, obj):
        return format_html("<a class='button' href='/admin/tickets/chat/{}/'>💬 مشاهده چت</a>", obj.id)

    view_chat_link.short_description = "چت"

    # region jalali_date_format
    def persian_created_at(self, obj):
        return format_jalali_dates_2(obj.created_at)

    persian_created_at.short_description = 'تاریخ ثبت'

    # endregion

    list_display = ['title', 'user', 'status', 'priority', 'section', 'ticket_code', 'persian_created_at', 'view_chat_link']
    list_filter = ['status', 'priority', 'ticket_code', 'section']
    list_editable = ['status']
    search_fields = ['title', 'user__username']
    readonly_fields = ['ticket_code']
