import enum

class ChangePasswordResult(enum.Enum):
    success = 'کلمه عبور شما با موفقیت تغییر یافت لطفا مجدد با همان کلمه عبور وارد حساب کاربری خود شوید!'
    error = 1