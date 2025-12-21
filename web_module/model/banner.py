from django.db import models

class BannerType(models.TextChoices):
    Slider = 'Slider', 'اسلایدر سایت'
    TopBanner = 'TopBanner', 'بنر وسط سایت'
    BottomBanner = 'BottomBanner','بنر پایین سایت'


class Banner(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان بنر")
    type = models.CharField(choices=BannerType, verbose_name="نوع بنر")
    image = models.ImageField(upload_to='images/products/', verbose_name='تصویر')
    url = models.URLField(null=True, blank=False,verbose_name='لینک بنر')
    is_active = models.BooleanField(default=False, verbose_name="فعال / غیر فعال")

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنر ها"

    def __str__(self):
        return f'{self.title} ({self.get_type_display()}) - {'فعال' if self.is_active else 'غیر فعال' }'