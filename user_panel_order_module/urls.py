from django.urls import path

from user_panel_order_module.views import *

urlpatterns = [
    path('', OrderListView.as_view(), name='user_panel_order_list_page'),
    path('d/<int:pk>', OrderDetailsView.as_view(), name='user_panel_order_details_page'),
]