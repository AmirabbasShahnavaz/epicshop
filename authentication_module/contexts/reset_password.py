from authentication_module.contexts.enums import ResetPasswordResult
from authentication_module.forms import ResetPasswordForm
from authentication_module.model import User


def reset_password_context(reset_password_form: ResetPasswordForm, mobile:str):
    otp_code = reset_password_form.cleaned_data.get('otp_code')
    password = reset_password_form.cleaned_data.get('password')
    if otp_code == '*****':
        return ResetPasswordResult.otp_code_empty

    user:User = User.objects.filter(mobile__exact=mobile, forgot_password_verify_code__exact=otp_code).first()
    if not user:
        return ResetPasswordResult.user_not_found

    user.is_active = True
    user.mobile_verify_code = None
    user.set_password(password)
    user.save()
    return ResetPasswordResult.success