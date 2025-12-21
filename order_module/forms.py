from django import forms


class OrderFillUserNameForm(forms.Form):
    first_name = forms.CharField(label="نام",max_length=150,min_length="3",widget=forms.TextInput(attrs={'class': 'ms-2 form-control w-20'}))
    last_name = forms.CharField(label="نام خانوادگی",max_length=150,min_length="3",widget=forms.TextInput(attrs={'class': 'ms-2 form-control w-20'}))