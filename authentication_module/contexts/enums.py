import enum

class RegisterResult(enum.Enum):
    success = 'ثبت نام شما با موفقیت انجام شد'
    mobile_exist = 'تلفن همراه وارد شده قبلا در سیستم ثبت شده است!'
    send_sms_failed = 'مشکلی در ارسال پیامک به وجود آمده لطفا دوباره تلاش کنین!'


class MobileActivationResult(enum.Enum):
    success = 'حساب شما با موفقیت فعال شد!'
    user_not_found = 'کاربری یافت نشد!'
    otp_code_empty = 'لطفا کد فعالسازی را وارد کنید!'


class LoginResult(enum.Enum):
    success = 'کاربر گرامی به سایت ما خوش آمدید!'
    user_not_found = 'کاربری با این مشخصات یافت نشد!'
    user_not_active = 'حساب کاربری شما فعال نمی باشد جهت فعالسازی میتونید از بخش فراموشی کلمه عبور اقدام کنید'

class LoginOtpResult(enum.Enum):
    success = 'کاربر گرامی به سایت ما خوش آمدید!'
    user_not_found = 'کاربری یافت نشد!'
    otp_code_empty = 'لطفا کد فعالسازی را وارد کنید!'


class ForgotPasswordResult(enum.Enum):
    success = 0
    user_not_found = 'کاربری با این مشخصات یافت نشد!'
    send_sms_failed = 'مشکلی در ارسال پیامک به وجود آمده لطفا دوباره تلاش کنین!'


class ResetPasswordResult(enum.Enum):
    success = 'بازیابی کلمه عبور با موفقیت انجام شد !'
    user_not_found = 'کاربری یافت نشد!'
    otp_code_empty = 'لطفا کد بازیابی را وارد کنید!'