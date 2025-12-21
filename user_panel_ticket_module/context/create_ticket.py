from enum import Enum

from django.db.models import Q
from django.http import HttpRequest

from user_panel_ticket_module.forms import CreateTicketForm, SendTicketMessageForm
from user_panel_ticket_module.model import TicketMessage, Ticket
from user_panel_ticket_module.model.choices import TicketStatus


class CreateTicketResult(Enum):
    success = 1,
    error = 2


def create_ticket_context(request: HttpRequest, create_ticket_form: CreateTicketForm,
                          message_form: SendTicketMessageForm):
    ticket_count = Ticket.objects.filter(user=request.user, status=TicketStatus.Pending).count()
    ticket_answered_by_user_count = Ticket.objects.filter(user=request.user, status=TicketStatus.AnsweredByUser).count()
    if ticket_count >= 3 or ticket_answered_by_user_count >= 3:
        return CreateTicketResult.error
    user = request.user
    ticket = create_ticket_form.save(commit=False)
    ticket.user = user
    create_ticket_form.save()

    new_ticket_message = TicketMessage(user=user, ticket=ticket, message=message_form.cleaned_data.get('message'))
    new_ticket_message.save()
    return CreateTicketResult.success
