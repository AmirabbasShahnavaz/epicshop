import jdatetime
from django import template

from helper_utils.jalalidate import format_jalali_dates_2

register = template.Library()


@register.filter
def to_shamsi(value):
    if not value:
        return ""

    # تبدیل میلادی به شمسی
    jdate = jdatetime.datetime.fromgregorian(datetime=value)

    # نام فارسی ماه‌ها
    persian_months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]

    month_name = persian_months[jdate.month - 1]

    # فرمت نهایی
    return f"{jdate.day} {month_name} {jdate.year} ساعت {jdate.hour:02}:{jdate.minute:02}"


@register.filter(name='wallet_badge_status')
def status_badge_class(status):
    return {
        'Deposit': 'success',
        'Creditor': 'danger',
    }.get(status, 'secondary')

@register.filter(name='ticket_badge_status')
def status_badge_class(status):
    return {
        'AnsweredByUser': 'secondary',
        'AnsweredByAdmin': 'success',
        'Closed': 'danger',
    }.get(status, 'secondary')


@register.filter
def get_pay_amount(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return ''
    tax_price = (value * 10) / 100
    return int(value + tax_price)


@register.filter
def persian_amount(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return ''

    # عدد کامل فارسی با جداکننده کاما
    formatted_number = format(value, ',')
    formatted_number = formatted_number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))

    # تعیین واحد درست
    if value >= 1_000_000_000:
        unit = 'میلیارد'
    elif value >= 1_000_000:
        unit = 'میلیون'
    elif value >= 1_000:
        unit = 'هزار'
    elif value > 0:
        unit = 'ریال'
    else:
        unit = ''

    if unit:
        return f'{formatted_number} ({unit})'
    else:
        return formatted_number


@register.filter
def jalali_format(value):
    if not value:
        return ''
    return format_jalali_dates_2(value)
