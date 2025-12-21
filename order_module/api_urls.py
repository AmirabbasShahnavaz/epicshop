from django.urls import path

from . import api_views

urlpatterns = [
    path('basket/increase-quantity/<int:product_id>/<int:color_id>', api_views.IncreaseBasketQuantityAPIView.as_view(), name='increase_basket_quantity_api'),
    path('basket/decrease-quantity/<int:product_id>/<int:color_id>', api_views.DecreaseBasketQuantityAPIView.as_view(), name='decrease_basket_quantity_api'),
    path('basket/destroy/<int:product_id>/<int:color_id>', api_views.DestroyBasketProductAPIView.as_view(), name='destroy_basket_product_api'),
]