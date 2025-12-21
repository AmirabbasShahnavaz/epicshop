from rest_framework import serializers

from product_module.model import Product
from product_module.model.product_color import ProductColor


class ProductAutoCompleteSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', default='بدون دسته‌بندی')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'category']



class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']

class ProductChangeColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['price']