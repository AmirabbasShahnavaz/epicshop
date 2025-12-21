from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ویژگی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'