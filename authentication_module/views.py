from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from authentication_module.contexts.enums import *
from authentication_module.contexts.forgot_password import forgot_password_context
from authentication_module.contexts.login import login_context
from authentication_module.contexts.login_otp import login_otp_context
from authentication_module.contexts.mobile_activation import mobile_activation_context
from authentication_module.contexts.register import register_context
from authentication_module.contexts.reset_password import reset_password_context
from authentication_module.forms import *
from helper_utils.auth import check_user_authenticated, get_mobile_show


# Create your views here.

class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        request.session.pop('mobile_activate', None)
        request.session.pop('mobile_otp', None)
        request.session.pop('mobile_forgot_password', None)
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/register.html', {'form': RegisterForm(), 'next_url': next_url})

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        next_url = request.POST.get('next')
        if register_form.is_valid():
            result = register_context(register_form)
            match result:
                case RegisterResult.success:
                    messages.success(request, RegisterResult.success.value)
                    request.session['mobile_activate'] = register_form.cleaned_data.get('mobile')
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(f"{reverse('mobile_activation_page')}?next={next_url}")
                    return redirect('mobile_activation_page')
                case RegisterResult.mobile_exist:
                    return render(request, 'authentication_module/register.html', {'form': register_form,
                                                                                   'error_message': RegisterResult.mobile_exist.value,
                                                                                   'next_url': next_url})
                case RegisterResult.send_sms_failed:
                    return render(request, 'authentication_module/register.html', {'form': register_form,
                                                                                   'error_message': RegisterResult.send_sms_failed.value,
                                                                                   'next_url': next_url})
        return render(request, 'authentication_module/register.html', {'form': register_form, 'next_url': next_url})


class MobileActivationView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        mobile = request.session.get('mobile_activate')
        if not mobile:
            request.session.pop('mobile_activate', None)
            raise Http404

        mobile_show = get_mobile_show(mobile)
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/mobile_activation.html',
                      {"form": MobileActivationForm(), "mobile_show": mobile_show, 'mobile': mobile,
                       'next_url': next_url})

    def post(self, request: HttpRequest):
        mobile = request.session.get('mobile_activate')
        if not mobile:
            request.session.pop('mobile_activate', None)
            raise Http404

        mobile_activation_form = MobileActivationForm(request.POST)
        next_url = request.POST.get('next')
        mobile_show = get_mobile_show(mobile)
        if mobile_activation_form.is_valid():
            result = mobile_activation_context(mobile_activation_form, mobile)
            match result:
                case MobileActivationResult.success:
                    request.session.pop('mobile_activate', None)
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(f"{reverse('login_page')}?next={next_url}")
                    return redirect('login_page')

                case MobileActivationResult.user_not_found:
                    return render(request, 'authentication_module/mobile_activation.html',
                                  {"form": mobile_activation_form, "mobile": mobile_show,
                                   "error_message": MobileActivationResult.user_not_found.value, 'next_url': next_url})

                case MobileActivationResult.otp_code_empty:
                    return render(request, 'authentication_module/mobile_activation.html',
                                  {"form": mobile_activation_form, "mobile": mobile_show,
                                   "error_message": MobileActivationResult.otp_code_empty.value, 'next_url': next_url})

        return render(request, 'authentication_module/mobile_activation.html',
                      {"form": mobile_activation_form, "mobile": mobile_show, 'next_url': next_url})


def redirect_home_page_view(request: HttpRequest):
    if not check_user_authenticated(request):
        request.session.pop('mobile_activate', None)
        request.session.pop('mobile_otp', None)
        request.session.pop('mobile_forgot_password', None)
    return redirect('home_page')


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        mobile_session = request.session.get('mobile_otp')
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/login.html',
                      {'form': LoginForm(), 'mobile_session': mobile_session, 'next_url': next_url})

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        next_url = request.POST.get('next')
        if login_form.is_valid():

            is_next_step = next_url == reverse('basket_next_step_page')
            if is_next_step:
                is_pay = True
            else:
                is_pay = False

            result = login_context(request, login_form, is_pay=is_pay)
            match result:
                case LoginResult.success:
                    messages.success(request, LoginResult.success.value)
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        if is_next_step:
                            messages.success(request, 'سفارش شما با موفقیت ثبت شد!')
                        return redirect(next_url)
                    return redirect('user_panel_home_page')

                case LoginResult.user_not_found:
                    return render(request, 'authentication_module/login.html',
                                  {'form': login_form, 'error_message': LoginResult.user_not_found.value,
                                   'next_url': next_url})

                case LoginResult.user_not_active:
                    return render(request, 'authentication_module/login.html', {'form': login_form,
                                                                                'error_message': LoginResult.user_not_active.value,
                                                                                'next_url': next_url})

        return render(request, 'authentication_module/login.html', {'form': login_form, 'next_url': next_url})


class LoginWithOtpView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        mobile = request.session.get('mobile_otp')
        if not mobile:
            request.session.pop('mobile_otp', None)
            raise Http404

        mobile_show = get_mobile_show(mobile)
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/login_otp.html',
                      {"form": LoginOtpForm(), "mobile_show": mobile_show, 'mobile': mobile, 'next_url': next_url})

    def post(self, request: HttpRequest):
        mobile = request.session.get('mobile_otp')
        if not mobile:
            request.session.pop('mobile_otp', None)
            raise Http404

        login_otp_form = LoginOtpForm(request.POST)
        mobile_show = get_mobile_show(mobile)
        next_url = request.POST.get('next')
        if login_otp_form.is_valid():

            is_next_step = next_url == reverse('basket_next_step_page')
            if is_next_step:
                is_pay = True
            else:
                is_pay = False

            result = login_otp_context(request, login_otp_form, mobile, is_pay=is_pay)
            match result:
                case LoginOtpResult.success:
                    request.session.pop('mobile_otp', None)
                    messages.success(request, LoginOtpResult.success.value)
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        if is_next_step:
                            messages.success(request, 'سفارش شما با موفقیت ثبت شد!')
                        return redirect(next_url)
                    return redirect('user_panel_home_page')
                case LoginOtpResult.user_not_found:
                    return render(request, 'authentication_module/login_otp.html',
                                  {"form": login_otp_form, "mobile": mobile_show,
                                   "error_message": LoginOtpResult.user_not_found.value, 'next_url': next_url})
                case LoginOtpResult.otp_code_empty:
                    return render(request, 'authentication_module/login_otp.html',
                                  {"form": login_otp_form, "mobile": mobile_show,
                                   "error_message": LoginOtpResult.otp_code_empty.value, 'next_url': next_url})
        return render(request, 'authentication_module/login_otp.html',
                      {"form": login_otp_form, "mobile": mobile_show, 'next_url': next_url})


class ForgotPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/forgot_password.html',
                      {'form': ForgotPasswordForm(), 'next_url': next_url})

    def post(self, request: HttpRequest):
        forgot_password_form = ForgotPasswordForm(request.POST)
        next_url = request.POST.get('next')
        if forgot_password_form.is_valid():
            result = forgot_password_context(request, forgot_password_form)
            match result:
                case ForgotPasswordResult.success:
                    request.session['mobile_forgot_password'] = forgot_password_form.cleaned_data.get('mobile')
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(f"{reverse('reset_password_page')}?next={next_url}")
                    return redirect('reset_password_page')
                case ForgotPasswordResult.user_not_found:
                    return render(request, 'authentication_module/forgot_password.html',
                                  {'form': forgot_password_form,
                                   'error_message': ForgotPasswordResult.user_not_found.value, 'next_url': next_url})

                case ForgotPasswordResult.send_sms_failed:
                    print(next_url)
                    return render(request, 'authentication_module/forgot_password.html', {'form': forgot_password_form,
                                                                                          'error_message': ForgotPasswordResult.send_sms_failed.value,
                                                                                          'next_url': next_url})

        return render(request, 'authentication_module/forgot_password.html',
                      {'form': forgot_password_form, 'next_url': next_url})


class ResetPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        mobile = request.session.get('mobile_forgot_password')
        if not mobile:
            request.session.pop('mobile_forgot_password', None)
            raise Http404

        mobile_show = get_mobile_show(mobile)
        next_url = request.GET.get('next', '')
        return render(request, 'authentication_module/reset_password.html',
                      {"form": ResetPasswordForm(), "mobile_show": mobile_show, 'mobile': mobile, 'next_url': next_url})

    def post(self, request: HttpRequest):
        mobile = request.session.get('mobile_forgot_password')
        if not mobile:
            request.session.pop('mobile_forgot_password', None)
            raise Http404

        reset_password_form = ResetPasswordForm(request.POST)
        mobile_show = get_mobile_show(mobile)
        next_url = request.POST.get('next')
        if reset_password_form.is_valid():
            result = reset_password_context(reset_password_form, mobile)
            match result:
                case ResetPasswordResult.success:
                    request.session.pop('mobile_forgot_password', None)
                    messages.success(request, ResetPasswordResult.success.value)
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(f"{reverse('login_page')}?next={next_url}")
                    return redirect('login_page')
                case ResetPasswordResult.user_not_found:
                    return render(request, 'authentication_module/reset_password.html',
                                  {"form": reset_password_form, "mobile": mobile_show,
                                   "error_message": ResetPasswordResult.user_not_found.value})
                case ResetPasswordResult.otp_code_empty:
                    return render(request, 'authentication_module/reset_password.html',
                                  {"form": reset_password_form, "mobile": mobile_show,
                                   "error_message": ResetPasswordResult.otp_code_empty.value})
        return render(request, 'authentication_module/reset_password.html',
                      {"form": reset_password_form, "mobile": mobile_show})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not check_user_authenticated(request):
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        logout(request)
        return redirect('home_page')
