from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils.timezone import localtime

from helper_utils.jalalidate import format_jalali_dates_2
from .model.choices import TicketStatus
from .models import Ticket, TicketMessage
import jdatetime


def is_admin(user):
    return user.is_staff or user.is_superuser


def ticket_chat(request, ticket_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/?next=' + request.path)

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not (request.user == ticket.user or request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("شما اجازه مشاهده این تیکت را ندارید.")

    if request.method == "POST":
        if ticket.status == 'Closed':
            return JsonResponse({"error": "این تیکت بسته شده است."}, status=403)

        message_text = request.POST.get('message', '').strip()
        if message_text:
            TicketMessage.objects.create(
                ticket=ticket,
                user=request.user,
                message=message_text,
                is_admin=request.user.is_staff or request.user.is_superuser
            )
        return JsonResponse({"success": True})

    # گرفتن پیام‌ها به ترتیب واقعی
    messages_qs = TicketMessage.objects.filter(ticket=ticket).select_related('user').order_by('created_at')
    messages = []
    for msg in messages_qs:
        created_str = format_jalali_dates_2(localtime(msg.created_at))
        user_full_name = msg.user.get_full_name() if msg.user.get_full_name() else None
        user_mobile = getattr(msg.user, 'mobile', '')
        messages.append({
            'id': msg.id,
            'message': msg.message,
            'is_admin': msg.is_admin,
            'created_at': created_str,
            'user_full_name': user_full_name,
            'user_mobile': user_mobile,
        })

    return render(request, 'tickets/chat.html', {
        'ticket': ticket,
        'messages': messages,
    })


def change_ticket_status(request, ticket_id, status):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin/login/?next=' + request.path)

    if not is_admin(request.user):
        return HttpResponseForbidden("شما اجازه تغییر وضعیت تیکت را ندارید.")

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status == 'Closed' and status != 'Closed':
        return HttpResponseForbidden("تیکت بسته شده و قابل تغییر نیست.")

    valid_statuses = [choice[0] for choice in TicketStatus.choices]
    if status not in valid_statuses:
        return HttpResponseForbidden("وضعیت نامعتبر است.")

    ticket.status = status
    ticket.save()
    return redirect('admin:user_panel_ticket_module_ticket_change', ticket.id)


def ticket_messages_api(request, ticket_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "ابتدا وارد شوید."}, status=403)

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not (request.user == ticket.user or is_admin(request.user)):
        return JsonResponse({"error": "دسترسی ندارید"}, status=403)

    messages_qs = TicketMessage.objects.filter(ticket=ticket).select_related('user').order_by('created_at')
    messages = []
    for msg in messages_qs:
        created_str = format_jalali_dates_2(localtime(msg.created_at))
        user_full_name = msg.user.get_full_name() if msg.user.get_full_name() else None
        user_mobile = getattr(msg.user, 'mobile', '')
        messages.append({
            'id': msg.id,
            'message': msg.message,
            'is_admin': msg.is_admin,
            'created_at': created_str,
            'user_full_name': user_full_name,
            'user_mobile': user_mobile,
        })
    return JsonResponse({'messages': messages})
