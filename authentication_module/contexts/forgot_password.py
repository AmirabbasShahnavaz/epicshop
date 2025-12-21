import random

from django.http import HttpRequest
from authentication_module.contexts.enums import ForgotPasswordResult
from authentication_module.forms import ForgotPasswordForm
from authentication_module.model import User
from helper_utils.send_sms import send_sms_with_template


def forgot_password_context(request : HttpRequest,forgot_password_form: ForgotPasswordForm):
    mobile = forgot_password_form.cleaned_data.get('mobile')
    user:User = User.objects.filter(mobile__exact=mobile).first()
    if not user:
        return ForgotPasswordResult.user_not_found

    verify_code = random.randrange(100000, 999999)
    sms_result = send_sms_with_template(
        mobile,
        'ResetPassVerification',
        str(verify_code),
    )
    if sms_result:
        user.forgot_password_verify_code = verify_code
        user.save()
        return ForgotPasswordResult.success
    else:
        return ForgotPasswordResult.send_sms_failed