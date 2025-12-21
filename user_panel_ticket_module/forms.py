from django import forms

from user_panel_ticket_module.model import Ticket
from user_panel_ticket_module.model.choices import TicketStatus


class CreateTicketForm(forms.ModelForm):
    title = forms.CharField(
        min_length=4,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان تیکت را وارد کنید...'}),
        label='عنوان تیکت'
    )

    class Meta:
        model = Ticket
        exclude = ['status', 'ticket_code', 'user']

        widgets = {
            "section": forms.Select(attrs={'class': 'form-select'}),
            "priority": forms.Select(attrs={'class': 'form-select'})
        }

        labels = {
            "section": "بخش مربوطه",
            "priority": "الویت"
        }


class SendTicketMessageForm(forms.Form):
    message = forms.CharField(label='متن پیام', min_length=4, max_length=800, widget=forms.Textarea(
        attrs={'class': 'form-control form-control-rounded py-3', 'placeholder': 'پیام خود را وارد کنید...',
               'rows': '7'}))
