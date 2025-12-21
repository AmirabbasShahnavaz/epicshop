# sms_helper.py
from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException

KAVENEGAR_API_KEY = settings.KAVENEGAR_API_KEY


def send_sms_with_template(phone: str, template: str, token: str, token2: str = None, token3: str = None):
    """
    ارسال پیامک با استفاده از قالب (template) در Kavenegar.

    پارامترها:
    - phone: شماره گیرنده (مثل '09121234567')
    - template: نام قالب در پنل Kavenegar
    - token: مقدار جایگزین {token} در متن قالب (اجباری)
    - token2: مقدار جایگزین {token2} در متن قالب (اختیاری)
    - token3: مقدار جایگزین {token3} در متن قالب (اختیاری)
    """
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'receptor': phone,
            'template': template,
            'token': token,
            'type': 'sms',
        }
        if token2:
            params['token2'] = token2
        if token3:
            params['token3'] = token3

        response = api.verify_lookup(params)
        return response

    except (APIException, HTTPException) as e:
        print(f"Kavenegar error: {e}")
        return None
