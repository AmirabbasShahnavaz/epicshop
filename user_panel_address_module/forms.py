import re

from django import forms
from django.core.exceptions import ValidationError

from user_panel_address_module.model.address import Address

phone_number_regex = r'^0\d{2}\d{8}$'
plate_number_and_home_unit_regex = r'^[1-9][0-9]*$'


class CreateOrUpdateAddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['full_address', 'user']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'برچسب آدرس خود را وارد کنید...'}),
            'plate_number': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'پلاک آدرس خود را وارد کنید ...'}),
            'home_unit': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'واحد آدرس خود را وارد کنید...'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'تلفن ثابت خود را با پیشوند وارد کنید...'}),
            'street_or_neighborhood': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'نام خیابان یا محله خود را وارد کنید..'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'اگر آدرس شما توصیحات خاصی دارد آن را وارد کنید...'}),
        }
        labels = {
            'label': 'برچسب',
            'plate_number': 'پلاک',
            'home_unit': 'واحد',
            'phone_number': 'تلفن ثابت',
            'street_or_neighborhood': 'خیابان یا محله',
            'description': 'توضیحات',
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        pattern = r'^0[1-8][0-9]{1,2}[0-9]{7}$'
        if not re.fullmatch(pattern, phone):
            raise ValidationError(
                "تلفن همراه وارد شده معتبر نمی باشد!")
        return phone