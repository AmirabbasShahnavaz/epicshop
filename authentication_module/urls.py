
from django.urls import path

from authentication_module.views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register_page'),
    path('mobile_activation', MobileActivationView.as_view(), name='mobile_activation_page'),
    path('mobile_activation/1fdb71114be07434c0cc', redirect_home_page_view, name='redirect_home_from_activation_page'),
    path('login', LoginView.as_view(), name='login_page'),
    path('login/otp', LoginWithOtpView.as_view(), name='login_otp_page'),
    path('forgot_pass', ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset_pass', ResetPasswordView.as_view(), name='reset_password_page'),
    path('logout', LogoutView.as_view(), name='logout_page'),
]