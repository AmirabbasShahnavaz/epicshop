from django.db import models
from django.utils.crypto import get_random_string
from django_ckeditor_5.fields import CKEditor5Field

from product_module.model.product_category import ProductCategory




class Product(models.Model):
   title = models.CharField(max_length=255, verbose_name=' نام محصول')
   description = CKEditor5Field(verbose_name='توضبحات')
   category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, verbose_name='دسته بندی')
   price = models.DecimalField(decimal_places=0, max_digits=9, verbose_name='قیمت')
   warranty_text = models.CharField(max_length=255, verbose_name='متن گارانتی')
   image = models.ImageField(upload_to='images/products/', verbose_name='تصویر')
   is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
   short_key = models.CharField(max_length=10,unique=True, verbose_name='کد مخصوص محصول')
   slug = models.SlugField(max_length=500,allow_unicode=True,unique=True, verbose_name='اسلاگ')
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
   updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")


   def get_first_gallery(self):
      return self.productgallery_set.order_by('created_at').first()

   def get_first_color(self):
      return self.productcolor_set.filter(quantity__gte=1).order_by('-created_at').first()


   class Meta:
      verbose_name = 'محصول'
      verbose_name_plural = 'محصولات'