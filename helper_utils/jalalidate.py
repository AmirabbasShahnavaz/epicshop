import jdatetime

WEEKDAYS_FA = [
    'دوشنبه', 'سه‌شنبه', 'چهارشنبه',
    'پنج‌شنبه', 'جمعه', 'شنبه', 'یکشنبه'
]

MONTHS_FA = [
    '', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
]


def format_jalali_dates(gregorian_datetime):
    jalali = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
    weekday = WEEKDAYS_FA[jalali.weekday()]
    month = MONTHS_FA[jalali.month]
    return f"{weekday} {jalali.day} {month} {jalali.year} _ ساعت {jalali.hour}:{str(jalali.minute).zfill(2)} دقیقه"


def format_jalali_dates_2(gregorian_datetime):
    jalali = jdatetime.datetime.fromgregorian(datetime=gregorian_datetime)
    month = MONTHS_FA[jalali.month]
    # تبدیل عدد روز و ساعت و دقیقه به رشته فارسی (اختیاری)
    day = str(jalali.day)
    hour = str(jalali.hour).zfill(2)
    minute = str(jalali.minute).zfill(2)
    return f"{day} {month} {jalali.year} - ساعت {hour}:{minute}"
