from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

from authentication_module.model import User


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'user_panel_module/widgets/custom_clearable_file_input.html'


class EditUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': CustomClearableFileInput
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'پست الکترونیکی',
            'avatar': 'آواتار',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='کلمه عبور فغلی',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'کلمه عبور فعلی خود را وارد کنید...'}))
    new_password = forms.CharField(label='کلمه عبور جدید',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'کلمه عبور جدید خود را وارد کنید...'}))
    confirm_new_password = forms.CharField(label='تکرار کلمه عبور جدید',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'تکرار کلمه عبور جدید خود را وارد کنید...'}))

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise ValidationError('کلمه عبور جدید با تکرار آن یکسان نمی باشد')
        return confirm_new_password