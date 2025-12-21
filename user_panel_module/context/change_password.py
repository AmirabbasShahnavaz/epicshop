from django.contrib.auth import logout
from django.http import HttpRequest

from authentication_module.model import User
from user_panel_module.context.enums import ChangePasswordResult
from user_panel_module.forms import ChangePasswordForm


def change_password_context(request: HttpRequest, user: User, change_password_form: ChangePasswordForm):
    current_password = change_password_form.cleaned_data.get('current_password')
    if not user.check_password(current_password):
        change_password_form.add_error('current_password','کلمه عبور فعلی وارد شده اشتباه می باشد')
        return ChangePasswordResult.error

    new_password = change_password_form.cleaned_data.get('new_password')
    if user.check_password(new_password):
        change_password_form.add_error('new_password', 'کلمه عبور جدیدی را وارد کنید')
        return ChangePasswordResult.error

    user.set_password(new_password)
    user.save()
    logout(request)
    return ChangePasswordResult.success