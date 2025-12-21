from django.db.models import Prefetch

from product_module.model import ProductCategory


def get_all_category_for_site_header():
    children_with_products_qs = ProductCategory.objects.filter(
        is_active=True,
        product__isnull=False
    ).distinct()

    main_categories = ProductCategory.objects.filter(
        parent__isnull=True,
        is_active=True
    ).prefetch_related(
        Prefetch('productcategory_set', queryset=children_with_products_qs, to_attr='children_with_products')
    )
    return main_categories