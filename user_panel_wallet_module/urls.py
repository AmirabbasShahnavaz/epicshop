from django.urls import path

from user_panel_wallet_module.views import *
urlpatterns = [
    path('', WalletListView.as_view(), name='user_panel_wallet_index_page'),
    path('wallet_zarinpal_callback', wallet_zarinpal_callback, name='user_panel_wallet_zarinpal_callback_page'),
    path('verify', WalletVerifyView.as_view(), name='user_panel_wallet_verify_page'),
]
