from django import forms

from product_module.model import ProductFeature
from product_module.model.product_color import ProductColor


class ProductColorAdminForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = '__all__'
        widgets = {
            'color_code': forms.TextInput(attrs={'type': 'color'})
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        color_code = cleaned_data.get('color_code')
        product = cleaned_data.get('product')

        if not product or not product.pk:
            return cleaned_data

        product_colors = ProductColor.objects.filter(product=product)

        if product_colors.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"نام رنگ '{name}' قبلاً برای این محصول ثبت شده است.")

        if product_colors.filter(color_code=color_code).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"کد رنگ '{color_code}' قبلاً برای این محصول ثبت شده است.")

        return cleaned_data


class ProductFeatureAdminForm(forms.ModelForm):
    class Meta:
        model = ProductFeature
        fields = '__all__'
