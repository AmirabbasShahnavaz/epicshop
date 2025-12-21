from django.db.models import Prefetch


def limited_prefetch_from_model(model, related_name, limit,order_by=None, filter_kwargs=None, to_attr=None):
    """
    ساخت یک Prefetch محدود برای رابطه‌های مرتبط با مدل داده‌شده.

    پارامترها:
    - model: مدل اصلی (مثلاً Product)
    - related_name: نام رابطه روی مدل اصلی (مثلاً 'features')
    - limit: تعداد آیتم‌هایی که باید prefetch بشن
    - filter_kwargs: دیکشنری فیلتر برای آیتم‌های مرتبط (اختیاری)
    - to_attr: اسم سفارشی برای ذخیره آیتم‌ها در مدل اصلی (اختیاری)

    استفاده:
        limited_prefetch_from_model(Product, 'features', 4, {'is_deleted': False})
    """
    if not hasattr(model, '_meta'):
        raise ValueError("Invalid model provided.")

    related_field = model._meta.get_field(related_name)
    related_model = related_field.related_model

    filter_kwargs = filter_kwargs or {}
    to_attr = to_attr or f"limited_{related_name}"
    order_by = order_by or 'id'

    queryset = related_model.objects.filter(**filter_kwargs).order_by(order_by)[:limit]

    return Prefetch(related_name, queryset=queryset, to_attr=to_attr)
