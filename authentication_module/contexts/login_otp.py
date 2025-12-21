from django.contrib.auth import login
from django.http import HttpRequest

from authentication_module.contexts.enums import MobileActivationResult, LoginOtpResult
from authentication_module.forms import MobileActivationForm, LoginOtpForm
from authentication_module.model import User
from helper_utils.basket import get_guest_id
from order_module.model import Basket


def login_otp_context(request: HttpRequest, login_otp_form: LoginOtpForm, mobile: str, is_pay: bool = False):
    otp_code = login_otp_form.cleaned_data.get('otp_code')
    if otp_code == '*****':
        return LoginOtpResult.otp_code_empty

    user: User = User.objects.filter(mobile__exact=mobile, otp_verify_code__exact=otp_code).first()
    if not user:
        return LoginOtpResult.user_not_found

    user.is_active = True
    user.otp_verify_code = None
    user.save()

    if is_pay:
        guest_id = get_guest_id(request)
        Basket.objects.filter(guest_id=guest_id).update(user=user, guest_id='')

    login(request, user)
    return LoginOtpResult.success
