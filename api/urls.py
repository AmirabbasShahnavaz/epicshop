from django.urls import path, include

urlpatterns = [
    path('authentication_module/', include('authentication_module.api_urls')),
    path('order_module/', include('order_module.api_urls')),
]