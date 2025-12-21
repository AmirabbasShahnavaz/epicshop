from django.urls import path

from user_panel_ticket_module.views import *

urlpatterns = [
    path('',TicketListView.as_view(), name='user_panel_ticket_list_page'),
    path('create',TicketCreateView.as_view(), name='user_panel_ticket_create_page'),
    path('cancel_ticket',CancelTicketView.as_view(), name='user_panel_ticket_cancel_page'),
    path('d/<str:ticket_code>',TicketDetailsView.as_view(), name='user_panel_ticket_details_page'),
]