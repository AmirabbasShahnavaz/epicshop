from django import forms
from django.core.exceptions import ValidationError


class WalletChargingForm(forms.Form):
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'قیمت برای شارژ کیف پول خود...'}),
        label='قیمت (تومان)')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 10000:
            raise ValidationError('حداقل مبلغ شارژ کیف پول 10,000 هزار تومان است!')
        if amount >= 100000000:
            raise ValidationError('حداکثر مبلغ شارژ کیف پول 100,000,000 میلیون تومان است!')
        return amount