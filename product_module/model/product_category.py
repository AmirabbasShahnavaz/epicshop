from django.db import models


class ProductCategory(models.Model):
    title = models.CharField(max_length=150, unique=True,verbose_name='عنوان')
    url_title = models.SlugField(max_length=300, null=True, blank=False, unique=True , allow_unicode=True, verbose_name='عنوان در url')
    parent = models.ForeignKey('self',null=True,blank=True, on_delete=models.SET_NULL, verbose_name='والد')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    image = models.ImageField(upload_to='images/categories/',null=True,blank=True, verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    def __str__(self):
        return f"({self.title})"

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصولات'