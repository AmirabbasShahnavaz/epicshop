import random
import re

from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from authentication_module.model import User
from helper_utils.send_sms import send_sms_with_template


class ResendMobileActivationCodeView(APIView):
    def get(self, request, phone: str):
        regex_pattern = r'^09\d{9}$'
        if not re.match(regex_pattern, phone):
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        user: User = User.objects.filter(mobile__exact=phone, is_active=False).first()
        if not user:
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        verify_code = random.randrange(10000, 99999)
        sms_result = send_sms_with_template(
            phone,
            'MobileVerification',
            str(verify_code),
        )
        if sms_result:
            user.mobile_verify_code = verify_code
            user.save()
            return Response({'status': 'success', 'message': 'پیامک با موفقیت ارسال شد'}, HTTP_200_OK)

        return Response(
            {'status': 'send_code_failed', 'message': 'ارسال پیامک با خطا مواجه شد لطفا دوباره امتحان کنید'},
            HTTP_200_OK)


class ResendResetPasswordCodeView(APIView):
    def get(self, request, phone: str):
        regex_pattern = r'^09\d{9}$'
        if not re.match(regex_pattern, phone):
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        user: User = User.objects.filter(mobile__exact=phone).first()
        if not user:
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        verify_code = random.randrange(100000, 999999)
        sms_result = send_sms_with_template(
            phone,
            'ResetPassVerification',
            str(verify_code),
        )
        if sms_result:
            user.mobile_verify_code = verify_code
            user.save()
            return Response({'status': 'success', 'message': 'پیامک با موفقیت ارسال شد'}, HTTP_200_OK)

        return Response(
            {'status': 'send_code_failed', 'message': 'ارسال پیامک با خطا مواجه شد لطفا دوباره امتحان کنید'},
            HTTP_200_OK)


class ResendOtpCodeView(APIView):
    def get(self, request, phone: str):
        regex_pattern = r'^09\d{9}$'
        if not re.match(regex_pattern, phone):
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        user: User = User.objects.filter(mobile__exact=phone).first()
        if not user:
            return Response({'status': 'user_not_found', 'message': "کاربری یافت نشد!"}, HTTP_200_OK)

        verify_code = random.randrange(10000, 99999)
        sms_result = send_sms_with_template(
            phone,
            'LoginOtpVerification',
            str(verify_code),
        )
        if sms_result:
            user.otp_verify_code = verify_code
            user.save()
            return Response({'status': 'success', 'message': 'پیامک با موفقیت ارسال شد'}, HTTP_200_OK)

        return Response(
            {'status': 'send_code_failed', 'message': 'ارسال پیامک با خطا مواجه شد لطفا دوباره امتحان کنید'},
            HTTP_200_OK)


class SetLoginOtpAPIView(APIView):
    def get(self, request, phone: str):
        regex_pattern = r'^09\d{9}$'
        if not re.match(regex_pattern, phone):
            return Response({'status': 'mobile_not_valid', 'message': 'تلفن همراه وارد شده معتبر نیست'})
        user = User.objects.filter(mobile__exact=phone).first()
        if not user:
            return Response({'status': 'user_not_found', 'message': 'کاربری با این مشخصات یافت نشد'})
        verify_code = random.randrange(10000, 99999)
        sms_result = 'success'
        if sms_result:
            user.otp_verify_code = verify_code
            user.save()
            request.session['mobile_otp'] = phone
            next_url = request.GET.get('next', '')
            # for validation host of next_url page
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return Response({'status': 'success', 'url': f'{reverse('login_otp_page')}?next={next_url}'})
            return Response({'status': 'success', 'url': reverse('login_otp_page')})
        else:
            return Response(
                {'status': 'sms_send_failed', 'message': 'مشکلی در ارسال پیامک به وجود آمده لطفا دوباره تلاش کنین!'})
