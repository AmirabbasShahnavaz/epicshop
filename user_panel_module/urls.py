from django.urls import path, include

from user_panel_module.views import *

urlpatterns = [
    path('', HomeUserView.as_view(), name='user_panel_home_page'),
    path('edit', EditUserView.as_view(), name='user_panel_edit_user_page'),
    path('favorite_products', FavoriteProductListView.as_view(), name='user_panel_favorite_products_page'),
    path('change_pass', ChangePasswordView.as_view(), name='user_panel_change_password_page'),
    path('addresses/', include('user_panel_address_module.urls')),
    path('orders/', include('user_panel_order_module.urls')),
    path('wallet/', include('user_panel_wallet_module.urls')),
    path('tickets/', include('user_panel_ticket_module.urls')),
]