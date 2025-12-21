from django.urls import path, re_path

from product_module.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('d/change_color/<int:product_color_id>/<int:product_id>', ProductChangeColorView.as_view(), name='product_change_color_json'),
    re_path(r'd/(?P<slug>[-\w]+)', ProductDetailsView.as_view(), name='product_details_page'),
    path('search', ProductSearchView.as_view(), name='product_search_json'),
    path('add_to_favorite/<int:product_id>', AddToUserFavoriteView.as_view(), name='product_add_to_favorite_page'),
    path('compare', CompareProductListView.as_view(), name='product_compare_list_page'),
    re_path(r'(?P<category>[-\w]+)', ProductListView.as_view(), name='product_list_category_page'),
]
