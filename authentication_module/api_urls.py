from django.urls import path

from authentication_module.api_views import *

urlpatterns = [
    path('resend_code/<str:phone>', ResendMobileActivationCodeView.as_view(), name='resend_mobile_activation_page'),
    path('resend_reset_code/<str:phone>', ResendResetPasswordCodeView.as_view(), name='resend_reset_code_page'),
    path('resend_otp_code/<str:phone>', ResendOtpCodeView.as_view(), name='resend_otp_code_page'),
    path('set_otp/<str:phone>', SetLoginOtpAPIView.as_view(), name='set_login_otp_page'),
]