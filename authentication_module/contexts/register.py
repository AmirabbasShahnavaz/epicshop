import random

from authentication_module.contexts.enums import RegisterResult
from authentication_module.forms import RegisterForm
from authentication_module.model import User


def register_context(register_form: RegisterForm):
    mobile = register_form.cleaned_data.get('mobile')
    password = register_form.cleaned_data.get('password')
    user_exist: bool = User.objects.filter(mobile__exact=mobile).exists()
    if user_exist:
        return RegisterResult.mobile_exist
    verify_code = random.randrange(10000, 99999)
    # sms_result = send_sms_with_template(
    #     mobile,
    #     'MobileVerification',
    #     str(verify_code),
    # )
    sms_result = 'success'
    if sms_result:
        user: User = User(mobile=mobile , username=mobile, is_active=False)
        user.mobile_verify_code = verify_code
        user.set_password(password)
        user.save()
        return RegisterResult.success
    else:
        return RegisterResult.send_sms_failed