from django.urls import path, include

from web_module.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('', include('authentication_module.urls')),
    path('', include('order_module.urls')),
    path('products/', include('product_module.urls')),
    path('user_panel/', include('user_panel_module.urls')),
]