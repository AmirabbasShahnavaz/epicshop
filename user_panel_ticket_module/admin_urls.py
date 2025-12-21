from django.urls import path
from user_panel_ticket_module import admin_views as views

urlpatterns = [
    path('chat/<int:ticket_id>/', views.ticket_chat, name='ticket_chat'),
    path('chat/<int:ticket_id>/change-status/<str:status>/', views.change_ticket_status, name='change_ticket_status'),
    path('chat/api/<int:ticket_id>/', views.ticket_messages_api, name='ticket_messages_api'),
]
