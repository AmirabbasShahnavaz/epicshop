from django.conf import settings
from django.db.models import Count, Q, OuterRef, DecimalField, Min, Max
from django.db.models.functions import Coalesce
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from product_module.model import Product, ProductCategory, FavoriteProduct, ProductCompare
from product_module.model.product_color import ProductColor
from product_module.model.serializers.product_serializers import ProductSearchSerializer, ProductChangeColorSerializer


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_module/product_list.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):

        # region contexts
        context = super().get_context_data(**kwargs)
        price_range = ProductColor.objects.filter(
            product__is_active=True,
            quantity__gte=1
        ).order_by('created_at').aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )

        context['filter_min_price'] = price_range['min_price'] or 0
        context['filter_max_price'] = price_range['max_price'] or 0

        context['site_title'] = settings.SITE_TITLE
        context['search'] = self.request.GET.get('q') or ''

        context['selected_min_price'] = self.request.GET.get('smin_price') or 0
        context['selected_max_price'] = self.request.GET.get('smax_price') or price_range['max_price'] or 0

        context['sort_by'] = self.request.GET.get('sort_by') or ''

        page_number = self.request.GET.get('page') or 1
        context['current_page'] = int(page_number)

        category_page = self.kwargs.get('category')
        if category_page:
            category = ProductCategory.objects.filter(url_title__exact=category_page).first()
            context['category_page'] = category
        # endregion

        return context

    def get_queryset(self, **kwargs):
        query = super().get_queryset().filter(is_active=True).annotate(
            available_colors=Count('productcolor', filter=Q(productcolor__quantity__gte=1))
        ).filter(available_colors__gte=1).prefetch_related('productcolor_set', 'productgallery_set')

        first_color_price = ProductColor.objects.filter(
            product=OuterRef('pk'),
            quantity__gte=1
        ).order_by().values('product').annotate(
            min_price=Min('price')
        ).values('min_price')[:1]

        query = query.annotate(
            first_color_price=Coalesce(first_color_price, 0, output_field=DecimalField())
        )

        # region filters

        # region search filter
        search = self.request.GET.get('q')
        if search:
            query = query.filter(title__icontains=search)
        # endregion

        # region sortBy filter
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            match sort_by:
                case 'newest':
                    query = query.order_by('-created_at')
                case 'cheapest':
                    query = query.order_by('price')
                case 'most_expensive':
                    query = query.order_by('-price')
        # endregion

        # region colors filter

        mobile_color = self.request.GET.get('m_color')
        if mobile_color and mobile_color != 'all':
            query = query.filter(productcolor__color_code__exact=mobile_color)

        desktop_color = self.request.GET.get('color')
        if desktop_color and desktop_color != 'all':
            query = query.filter(productcolor__color_code__exact=desktop_color)
        # endregion

        # region price filter

        selected_min_price = self.request.GET.get('smin_price')
        selected_max_price = self.request.GET.get('smax_price')
        if selected_min_price is not None and selected_max_price is not None:
            query = query.filter(
                first_color_price__gte=selected_min_price,
                first_color_price__lte=selected_max_price
            )
        # endregion

        # region category filter
        category = self.kwargs.get('category')
        if category is not None:
            query = query.filter(category__url_title__exact=category)
        else:
            mobile_cats = self.request.GET.getlist('m_category')
            desktop_cats = self.request.GET.getlist('category')
            selected_categories = list(set(mobile_cats + desktop_cats))

            if selected_categories:
                query = query.filter(category__title__in=selected_categories).distinct()
        # endregion
        # endregion

        return query


def filter_side_component(request: HttpRequest, **kwargs):
    # region datas
    categories = ProductCategory.objects.filter(parent__isnull=False, is_active=True,
                                                product__isnull=False).annotate(
        product_count=Count('product')).distinct()

    colors = ProductColor.objects.filter(quantity__gte=1).values('name', 'color_code').distinct()
    # endregion

    context = {
        'categories': categories,
        'colors': colors,
        'selected_color': request.GET.get('color') or 'all',
        'selected_categories': request.GET.getlist('category'),
    }

    return render(request, 'product_module/includes/components/filter_side.html', context)


def mobile_filter_side_component(request, **kwargs):
    # region datas
    categories = ProductCategory.objects.filter(parent__isnull=False, is_active=True,
                                                product__isnull=False).annotate(
        product_count=Count('product')).distinct()

    colors = ProductColor.objects.filter(quantity__gte=1).values('name', 'color_code').distinct()
    # endregion

    context = {
        'categories': categories,
        'colors': colors,
        'selected_color': request.GET.get('m_color') or 'all',
        'selected_categories': request.GET.getlist('m_category'),
    }

    return render(request, 'product_module/includes/components/mobile_filter_side.html', context)


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'product_module/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_seller_name'] = settings.SITE_SELLER_NAME
        if self.request.user.is_authenticated:
            is_favorite = FavoriteProduct.objects.filter(
                user=self.request.user,
                product=self.object,
                is_delete=False
            ).exists()
        else:
            is_favorite = False

        context['is_favorite'] = is_favorite
        related_products = Product.objects.filter(category_id=self.object.category_id).prefetch_related(
            'productcolor_set',
            'productgallery_set').exclude(
            id=self.object.id)
        context['related_products'] = related_products
        return context

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(is_active=True).prefetch_related(
            'productcolor_set',
            'productgallery_set'
        )


def related_product_component_view(request, product: Product):
    related_products = Product.objects.filter(category_id=product.category_id).prefetch_related('productcolor_set',
                                                                                                'productgallery_set').exclude(
        id=product.id)
    context = {
        'related_products': related_products,
    }
    return render(request, 'product_module/includes/components/related_products.html', context)


class ProductSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        if not query or len(query) < 2:
            return Response([])
        products = Product.objects.filter(title__icontains=query, is_active=True)[:10]
        serializer = ProductSearchSerializer(products, many=True)
        return Response(serializer.data)


class ProductChangeColorView(APIView):
    def get(self, request, product_color_id, product_id):
        product_color = ProductColor.objects.filter(product__id=product_id, pk=product_color_id).first()
        if product_color:
            serializer = ProductChangeColorSerializer(product_color)
            return Response(serializer.data)
        return Response({'status': 'failed'})


class AddToUserFavoriteView(APIView):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response({'status': 'is_not_authenticated',
                             'message': 'برای افزودن محصول به علاقه مندی ها ابتدا باید وارد حساب کاربری خود شوید!'},
                            HTTP_200_OK)
        product_exists = Product.objects.filter(id=product_id, is_active=True).exists()
        if not product_exists:
            return Response({'status': 'product_not_found', 'message': 'محصولی یافت نشد!'}, HTTP_200_OK)

        favorite_product_exist = FavoriteProduct.objects.filter(user=request.user, product_id=product_id).first()
        if favorite_product_exist:
            if favorite_product_exist.is_delete:
                favorite_product_exist.is_delete = False
                favorite_product_exist.save()
                return Response(
                    {'status': 'success', 'message': 'محصول مورد نظر با موفقیت به علاقه مندی های شما اضافه شد !'},
                    HTTP_200_OK)

            favorite_product_exist.is_delete = True
            favorite_product_exist.save()
            return Response(
                {'status': 'success', 'message': 'محصول مورد نظر با موفقیت از علاقه مندی های شما حذف شد !'},
                HTTP_200_OK)

        new_favorite_product = FavoriteProduct.objects.create(user=request.user, product_id=product_id)
        new_favorite_product.save()

        return Response({'status': 'success', 'message': 'محصول مورد نظر با موفقیت به علاقه مندی های شما اضافه شد !'},
                        HTTP_200_OK)


class AddToCompareProductList(APIView):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            compare_exist = ProductCompare.objects.filter(user=request.user, product_id=product_id).exists()
            if compare_exist:
                return Response({'status': 'redirect_compare_page'}, HTTP_200_OK)

        else:
            pass


class CompareProductListView(View):
    def get(self, request):
        return render(request, "product_module/compare_product_list.html", {})
