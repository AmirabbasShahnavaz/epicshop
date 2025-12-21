from django.urls import path

from order_module.views import *

urlpatterns = [
    path('add_to_basket', AddToBasketView.as_view(), name='add_to_basket_page'),
    path('basket', BasketView.as_view(), name='basket_page'),
    path('basket/next_step', AddToOrderView.as_view(), name='basket_next_step_page'),
    path('order', OrderView.as_view(), name='order_page'),
    path('order/destroy_item', DestroyOrderView.as_view(), name='order_destroy_order_item_page'),
    path('order/canceling', CancelingOrderView.as_view(), name='order_canceling_page'),
    path('order/zarinpal_callback', order_zarinpal_callback, name='order_zarinpal_callback_page'),
    path('order/verify', OrderVerifyView.as_view(), name='order_payment_verify_page'),
]
