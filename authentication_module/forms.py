from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

mobile_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='تلفن همراه وارد شده معتبر نمی باشد'
)


# ---------------------Register Form---------------------
class RegisterForm(forms.Form):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[mobile_validator],
                             label='تلفن همراه خود را وارد کنید')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='کلمه عبور خود را وارد کنید')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='تکرار کلمه عبور خود را وارد کنید')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور با تکرار آن یکسان نیست')


# ---------------------MobileActivation Form---------------------
class MobileActivationForm(forms.Form):
    otp_code = forms.CharField(widget=forms.HiddenInput(attrs={"placeholder": "_", "id": "otp-value"}))

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if len(otp_code) == 5:
            return otp_code
        raise ValidationError('کد وارد شده معتبر نمی باشد')


# ---------------------Login Form---------------------
class LoginForm(forms.Form):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[mobile_validator],
                             label='تلفن همراه خود را وارد کنید')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='کلمه عبور')


# ---------------------LoginOtp Form---------------------
class LoginOtpForm(forms.Form):
    otp_code = forms.CharField(widget=forms.HiddenInput(attrs={"placeholder": "_", "id": "otp-value"}))

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if len(otp_code) == 5:
            return otp_code
        raise ValidationError('کد وارد شده معتبر نمی باشد')


# ---------------------ForgotPassword Form---------------------
class ForgotPasswordForm(forms.Form):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[mobile_validator],
                             label='تلفن همراه خود را وارد کنید')


# ---------------------ForgotPassword Form---------------------
class ResetPasswordForm(forms.Form):
    otp_code = forms.CharField(widget=forms.HiddenInput(attrs={"placeholder": "_", "id": "otp-value"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='کلمه عبور خود را وارد کنید')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label='تکرار کلمه عبور خود را وارد کنید')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور با تکرار آن یکسان نیست')

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if len(otp_code) == 6:
            return otp_code
        raise ValidationError('کد وارد شده معتبر نمی باشد')
