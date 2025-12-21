from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count, Prefetch, Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from authentication_module.model import User
from helper_utils.basket import get_guest_id, get_all_total_price
from helper_utils.daily_data import get_dollar_today, get_dollar_today_2
from helper_utils.product import get_all_category_for_site_header
from helper_utils.wallet import get_all_wallet_balance_amount
from order_module.model import Order, Basket, OrderItem
from order_module.model.choices import OrderStatus
from product_module.model import FavoriteProduct, Product, ProductCategory
from web_module.model.banner import Banner, BannerType


# Create your views here.

class HomeView(TemplateView):
    template_name = 'web_module/index.html'
    extra_context = {'site_title': settings.SITE_TITLE}


# -----------------------Render UserPanel Components------------------------------
@login_required
def user_panel_sidebar_component_view(request):
    user: User = User.objects.filter(id=request.user.id).first()
    total_wallet_balance_amount = get_all_wallet_balance_amount(request.user.id)
    return render(request, 'user_panel/partials/components/user_panel_sidebar_component.html',
                  {'user': user, 'total_wallet_balance_amount': total_wallet_balance_amount})


@login_required
def user_panel_mobile_sidebar_component_view(request):
    user: User = User.objects.filter(id=request.user.id).first()
    total_wallet_balance_amount = get_all_wallet_balance_amount(request.user.id)
    return render(request, 'user_panel/partials/components/user_panel_mobile_sidebar_component.html',
                  {'user': user, 'total_wallet_balance_amount': total_wallet_balance_amount})


# -----------------------Render Shared Components------------------------------

def footer_component(request):
    return render(request, 'partials/components/footer.html', {})


def header_component(request):
    search = request.GET.get('q')
    main_categories = get_all_category_for_site_header()

    order_items = None
    user = None
    user_favorite_products_count = 0
    if request.user.is_authenticated:
        user: User = User.objects.filter(id=request.user.id).first()
        user_order = Order.objects.filter(user=user, status=OrderStatus.PENDING).first()
        order_items = OrderItem.objects.filter(order=user_order)
        user_basket = Basket.objects.filter(user=user)
        user_favorite_products_count = FavoriteProduct.objects.filter(user=user, is_delete=False).count()
    else:
        user_order = Order.objects.filter(user=user, status=OrderStatus.PENDING).first()
        if user_order:
            order_items = OrderItem.objects.filter(order=user_order)
        guest_id = get_guest_id(request)
        user_basket = Basket.objects.filter(guest_id=guest_id)

    context = {'user': user, 'search': search, 'main_categories': main_categories,
               'user_order': user_order, 'order_items': order_items,
               'user_basket': user_basket, 'user_favorite_products_count': user_favorite_products_count}

    return render(request, 'partials/components/header.html', context)


def cart_convas_basket_component_view(request):
    order_items = None
    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user, status=OrderStatus.PENDING).first()
        order_items = OrderItem.objects.filter(order=user_order)
        user_basket = Basket.objects.filter(user=request.user)
    else:
        user_order = Order.objects.filter(user=None, status=OrderStatus.PENDING).first()
        if user_order:
            order_items = OrderItem.objects.filter(order=user_order)
        guest_id = get_guest_id(request)
        user_basket = Basket.objects.filter(guest_id=guest_id)

    total_price = get_all_total_price(user_basket)

    context = {'user_order': user_order, 'order_items': order_items, 'user_basket': user_basket,
               'basket_total_price': total_price}
    return render(request, 'partials/components/cart_convas_basket.html', context)


# -----------------------Render IndexPage Components------------------------------

def amazing_products_slider_component(request):
    return render(request, 'partials/components/amazing_products_slider.html', {})


def amazing_products_slider_2_component(request):
    return render(request, 'partials/components/amazing_products_slider_2.html', {})


def best_seller_products_component(request):
    order_items_qs = OrderItem.objects.filter(order__status=OrderStatus.PAID)

    top_products = (
        Product.objects.filter(
            products__in=order_items_qs
        )
        .annotate(order_count=Count('products'))
        .prefetch_related(
            'productcolor_set',
            'productgallery_set',
            Prefetch('products', queryset=order_items_qs.select_related('order'))
        )
        .order_by('-order_count')[:8]
    )

    return render(request, 'partials/components/best_seller_products.html', {'best_seller_products' : top_products})


def bottom_banners_component(request):
    bottom_banners = Banner.objects.filter(type=BannerType.BottomBanner)[:2]
    return render(request, 'partials/components/bottom_banners.html', {'bottom_banners': bottom_banners})


def cart_convas_basket_component(request):
    return render(request, 'partials/components/cart_convas_basket.html', {})


def category_slider_component(request):
    categories = ProductCategory.objects.filter(parent__isnull=False, is_active=True,
                                                product__isnull=False).annotate(
        product_count=Count('product')).distinct()

    return render(request, 'partials/components/category_slider.html', {'categories' : categories})


def newest_products_component(request):
    # فقط دسته‌بندی‌های فرزند که حداقل یک محصول فعال دارند
    categories = ProductCategory.objects.filter(
        parent__isnull=False,
        is_active=True
    ).annotate(
        active_products_count=Count('product', filter= Q(product__is_active=True))
    ).filter(
        active_products_count__gt=0
    ).prefetch_related(
        Prefetch(
            'product_set',
            queryset=Product.objects.filter(is_active=True).order_by('-created_at')
            .prefetch_related(
                'productcolor_set',
                'productgallery_set'
            ),
            to_attr='products'
        )
    )

    context = {
        'categories': categories,
    }
    return render(request, 'partials/components/newest_products.html', context)


def main_sliders_component(request):
    sliders = Banner.objects.filter(type=BannerType.Slider)[:4]
    instant_offer_products = Product.objects.filter(is_active=True).annotate(
        available_colors=Count('productcolor', filter=Q(productcolor__quantity__gte=1))
    ).filter(available_colors__gte=1).order_by('-created_at')[:4]

    return render(request, 'partials/components/main_sliders.html',
                  {"sliders": sliders, "instant_offer_products": instant_offer_products})


def middle_banners_component(request):
    middle_banners = Banner.objects.filter(type=BannerType.TopBanner)[:2]
    return render(request, 'partials/components/middle_banners.html', {'middle_banners': middle_banners})
