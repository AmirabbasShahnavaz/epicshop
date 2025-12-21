from authentication_module.contexts.enums import MobileActivationResult
from authentication_module.forms import MobileActivationForm
from authentication_module.model import User


def mobile_activation_context(mobile_activation_form: MobileActivationForm, mobile:str):
    otp_code = mobile_activation_form.cleaned_data.get('otp_code')
    if otp_code == '*****':
        return MobileActivationResult.otp_code_empty

    user:User = User.objects.filter(mobile__exact=mobile, is_active=False, mobile_verify_code__exact=otp_code).first()
    if not user:
        return MobileActivationResult.user_not_found

    user.is_active = True
    user.mobile_verify_code = None
    user.save()
    return MobileActivationResult.success