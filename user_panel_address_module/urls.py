from django.urls import path

from user_panel_address_module.views import *

urlpatterns = [
    path('', AddressListView.as_view(), name='user_panel_address_list_page'),
    path('load_cities/<int:state_id>', load_cities_view, name='user_panel_address_load_cities_page'),
    path('create', CreateAddressView.as_view(), name='user_panel_address_create_page'),
    path('edit/<int:address_id>', UpdateAddressView.as_view(), name='user_panel_address_edit_page'),
    path('delete/<int:address_id>', delete_address_view, name='user_panel_address_delete_page'),
    path('activate/<int:address_id>', activate_address_view, name='user_panel_address_activate_page'),
]
