from django.contrib.auth import login
from django.http import HttpRequest
from authentication_module.contexts.enums import LoginResult
from authentication_module.forms import RegisterForm, LoginForm
from authentication_module.model import User
from helper_utils.basket import get_guest_id
from order_module.model import Basket


def login_context(request: HttpRequest, login_form: LoginForm, is_pay: bool = False):
    mobile = login_form.cleaned_data.get('mobile')
    password = login_form.cleaned_data.get('password')

    user: User = User.objects.filter(mobile=mobile).first()
    if not user:
        return LoginResult.user_not_found
    if not user.check_password(password):
        return LoginResult.user_not_found

    if not user.is_active:
        return LoginResult.user_not_active

    if is_pay:
        guest_id = get_guest_id(request)
        Basket.objects.filter(guest_id=guest_id).update(user=user, guest_id='')

    login(request, user)

    return LoginResult.success
