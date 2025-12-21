from django.http import HttpRequest

from user_panel_module.forms import EditUserModelForm


def edit_user_context(edit_user_form:EditUserModelForm):
    # instance = edit_user_form.save(commit=False)
    # instance.is_email_active = True
    # instance.save()
    edit_user_form.save()
