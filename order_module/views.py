from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from helper_utils.basket import get_guest_id, get_all_total_price, get_pay_amount, get_tax_amount
from helper_utils.payment import order_verify_payment, order_payment_gateway
from helper_utils.wallet import get_all_wallet_balance_amount
from order_module.forms import OrderFillUserNameForm
from order_module.model import Basket, Order, OrderItem, OrderTransaction
from order_module.model.choices import OrderStatus
from product_module.model import Product
from product_module.model.product_color import ProductColor
from user_panel_address_module.model import Address
from user_panel_wallet_module.model import Wallet
from user_panel_wallet_module.model.wallet import WalletStatus


# Create your views here.

class AddToBasketView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user_order = Order.objects.filter(user=request.user, status=OrderStatus.PENDING).first()
            if user_order:
                messages.warning(request, 'لطفا ابتدا سبد خرید فعلی خود تکمیل و پرداخت کنید یا از آن انصراف دهید ')
                return redirect('order_page')

        product_id = request.POST.get('p_id')
        color_id = request.POST.get('c_id')
        if product_id and color_id:
            product = get_object_or_404(Product, pk=product_id)
            product_color = get_object_or_404(ProductColor, pk=color_id)
            basket_item = self.get_or_create_basket_item(request, product, product_color)
            if basket_item != None:
                if basket_item.quantity < basket_item.product_color.quantity:
                    basket_item.quantity += 1
                    basket_item.save()
                    messages.success(request, 'محصول شما با موفقیت به سبد خرید اضافه شد!')

                return redirect('basket_page')

            messages.warning(request, f'موجودی رنگ {product_color.name} برای این محصول به اتمام رسیده است')
            return redirect('product_details_page', slug=product.slug)
        raise Http404

    def get_or_create_basket_item(self, request: HttpRequest, product: Product, product_color: ProductColor):

        if product_color.quantity < 1:
            return None

        if request.user.is_authenticated:
            return Basket.objects.get_or_create(user=request.user, product=product, product_color=product_color)[0]
        # سشن کاربری که لاگین نکرده رو میگیریم یا اونو میسازیم چون الزامی هست
        guest_id = get_guest_id(request)
        return Basket.objects.get_or_create(guest_id=guest_id, product=product, product_color=product_color)[0]


class BasketView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if request.user.is_authenticated:
            basket_items = Basket.objects.filter(user=request.user)
        else:
            guest_id = get_guest_id(request)
            basket_items = Basket.objects.filter(guest_id=guest_id)

        total_price = get_all_total_price(basket_items)

        context = {'basket_items': basket_items,
                   'site_seller_name': settings.SITE_SELLER_NAME, 'total_price': total_price}
        return render(request, 'order_module/basket.html', context)


class AddToOrderView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'برای تکمیل فرایند خرید ابتدا وارد حساب کاربری خود شوید!')
            return redirect(f'{reverse('login_page')}?next={reverse('basket_next_step_page')}')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        active_address = Address.objects.filter(is_active=True, user_id=request.user.id).first()
        if not active_address:
            messages.warning(request, 'لطفا برای تکمیل خرید یک آدرسی برای ارسال بسازید!')
            return redirect(f'{reverse('user_panel_address_create_page')}?next={reverse('basket_next_step_page')}')

        basket_items = Basket.objects.filter(user=request.user)

        if not basket_items:
            messages.warning(request, "سبد خرید شما خالی می باشد !")
            return redirect('product_list_page')

        total_price = get_all_total_price(basket_items)
        new_order = Order.objects.create(
            user=request.user,
            amount=total_price,
            address=active_address,
        )
        new_order.save()

        for basket_item in basket_items:
            if basket_item.quantity <= basket_item.product_color.quantity and basket_item.product_color.quantity >= 1:
                new_order_item = OrderItem.objects.create(
                    order=new_order,
                    product=basket_item.product,
                    product_color=basket_item.product_color,
                    price=basket_item.product.price,
                    quantity=basket_item.quantity,
                )
                new_order_item.save()
        basket_items.delete()
        find_order_items = OrderItem.objects.filter(order=new_order).first()
        if find_order_items:
            messages.success(request, 'سفارش شما با موفقیت ثبت شد!')
            return redirect('order_page')

        Order.objects.filter(id=new_order.id).delete()
        OrderItem.objects.filter(order=new_order).delete()
        messages.warning(request,
                         'متسفانه موجودی رنگ های محصولات انتخاب شده به اتمام رسیده است لطفا محصولات دیگری را برای خرید انتخاب کنید با تشکر!')
        return redirect('basket_page')


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, request):
        user_order = Order.objects.filter(user=request.user, status=OrderStatus.PENDING).prefetch_related(
            'orders').first()
        if not user_order:
            raise Http404
        order_fill_username_form = OrderFillUserNameForm()
        if user_order.user.first_name:
            order_fill_username_form = None

        print(order_fill_username_form)

        user_balance_amount = get_all_wallet_balance_amount(request.user.id)
        tax_price = get_tax_amount(user_order.amount)
        order_items_amount = get_all_total_price(OrderItem.objects.filter(order=user_order))
        return render(request, 'order_module/order.html',
                      {'user_order': user_order, 'tax_price': tax_price,
                       'user_balance_amount': user_balance_amount, 'order_items_amount': order_items_amount,
                       'form': order_fill_username_form})

    def post(self, request: HttpRequest):
        user_order = get_object_or_404(Order, user=request.user, status=OrderStatus.PENDING)
        pay_method = request.POST.get('pay_method')

        if not user_order.user.first_name:
            order_fill_username_form = OrderFillUserNameForm(request.POST)
            if not order_fill_username_form.is_valid():
                user_balance_amount = get_all_wallet_balance_amount(request.user.id)
                tax_price = get_tax_amount(user_order.amount)
                order_items_amount = get_all_total_price(OrderItem.objects.filter(order=user_order))
                return render(request, 'order_module/order.html', {'user_order': user_order, 'tax_price': tax_price,
                                                                   'user_balance_amount': user_balance_amount,
                                                                   'order_items_amount': order_items_amount,
                                                                   'form': order_fill_username_form})
            else:
                if not pay_method and pay_method == '':
                    messages.error(request, 'لطفا روش پرداختی را انتخاب کنید!')
                    return redirect('order_page')

                can_pay_order_item_count = 0
                order_items = OrderItem.objects.filter(order=user_order)
                for order_item in order_items:
                    if order_item.quantity > order_item.product_color.quantity or order_item.product_color.quantity <= 0:
                        can_pay_order_item_count += 1
                if order_items.count() == can_pay_order_item_count:
                    user_order.delete()
                    order_items.delete()
                    messages.warning(request,
                                     'متسفانه موجودی رنگ های محصولات انتخاب شده به اتمام رسیده است لطفا محصولات دیگری را برای خرید انتخاب کنید با تشکر!')
                    return redirect('basket_page')

                pay_amount = get_pay_amount(user_order.amount)

                if pay_method == 'pay_wallet':
                    user_balance_amount = get_all_wallet_balance_amount(request.user.id)
                    if user_balance_amount < pay_amount:
                        messages.error(request, 'موجودی کیف پول شما برای پرداخت این سفارش کافی نیست!')
                        return redirect('order_page')
                    Wallet.objects.create(user=request.user, amount=pay_amount, status=WalletStatus.Creditor,
                                          description='پرداخت سفارش')
                    user_order.status = OrderStatus.PAID
                    user_order.user.first_name = order_fill_username_form.cleaned_data.get('first_name')
                    user_order.user.last_name = order_fill_username_form.cleaned_data.get('last_name')
                    user_order.user.save()
                    user_order.save()
                    messages.success(request, 'سفارش شما با موفقیت پرداخت شد و مبلغ پرداختی از کیف پول شما کسر گردید!')
                    return redirect('user_panel_order_list_page')

                user_order.user.first_name = order_fill_username_form.cleaned_data.get('first_name')
                user_order.user.last_name = order_fill_username_form.cleaned_data.get('last_name')
                user_order.user.save()

                new_order_transaction = OrderTransaction.objects.create(order=user_order, amount=pay_amount)
                new_order_transaction.save()

                ipg_url = order_payment_gateway(site_domain=settings.SITE_DOMAIN,
                                                order_transaction=new_order_transaction)
                if ipg_url is None:
                    messages.error(request, 'خطا در ارسال به درگاه')
                    return redirect('order_page')

                return redirect(ipg_url)

        if not pay_method and pay_method == '':
            messages.error(request, 'لطفا روش پرداختی را انتخاب کنید!')
            return redirect('order_page')

        can_pay_order_item_count = 0
        order_items = OrderItem.objects.filter(order=user_order)
        for order_item in order_items:
            if order_item.quantity > order_item.product_color.quantity or order_item.product_color.quantity <= 0:
                can_pay_order_item_count += 1
        if order_items.count() == can_pay_order_item_count:
            user_order.delete()
            order_items.delete()
            messages.warning(request,
                             'متسفانه موجودی رنگ های محصولات انتخاب شده به اتمام رسیده است لطفا محصولات دیگری را برای خرید انتخاب کنید با تشکر!')
            return redirect('basket_page')

        pay_amount = get_pay_amount(user_order.amount)

        if pay_method == 'pay_wallet':
            user_balance_amount = get_all_wallet_balance_amount(request.user.id)
            if user_balance_amount < pay_amount:
                messages.error(request, 'موجودی کیف پول شما برای پرداخت این سفارش کافی نیست!')
                return redirect('order_page')
            Wallet.objects.create(user=request.user, amount=pay_amount, status=WalletStatus.Creditor,
                                  description='پرداخت سفارش')
            user_order.status = OrderStatus.PAID
            user_order.user.save()
            user_order.save()
            messages.success(request, 'سفارش شما با موفقیت پرداخت شد و مبلغ پرداختی از کیف پول شما کسر گردید!')
            return redirect('user_panel_order_list_page')

        new_order_transaction = OrderTransaction.objects.create(order=user_order, amount=pay_amount)
        new_order_transaction.save()

        ipg_url = order_payment_gateway(site_domain=settings.SITE_DOMAIN,
                                        order_transaction=new_order_transaction)
        if ipg_url is None:
            messages.error(request, 'خطا در ارسال به درگاه')
            return redirect('order_page')

        return redirect(ipg_url)


@method_decorator(login_required, name='dispatch')
class DestroyOrderView(View):
    def post(self, request: HttpRequest):
        user_order = get_object_or_404(Order, user=request.user, status=OrderStatus.PENDING)
        order_item_id = request.POST.get('o_item_id')
        order_item = OrderItem.objects.filter(order=user_order, id=order_item_id).first()
        if not order_item:
            messages.error(request, 'سفارشی یافت نشد!')
            return redirect('order_page')
        order_item.delete()
        messages.success(request, 'محصول مورد نظر با موفقیت از سفارش شما حذف گردید!')
        return redirect('order_page')


@method_decorator(login_required, name='dispatch')
class CancelingOrderView(View):
    def post(self, request: HttpRequest):
        user_order = get_object_or_404(Order, user=request.user, status=OrderStatus.PENDING)
        user_order.status = OrderStatus.CANCELED
        user_order.save()
        messages.success(request, 'شما با موفقیت از سفارش خود انصراف دادید!')
        return redirect('basket_page')


def order_zarinpal_callback(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if authority != '' and status != '':
        request.session["Authority"] = authority
        request.session["Status"] = status
        return redirect('order_payment_verify_page')


class OrderVerifyView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        authority = request.session.get('Authority')
        status = request.session.get('Status')
        if authority is not None and status is not None:
            order_transaction = OrderTransaction.objects.filter(authority__exact=authority).first()
            if not order_transaction:
                request.session.pop("Authority", None)
                request.session.pop("Status", None)
                raise Http404

            if order_transaction.status == OrderStatus.PENDING:
                if status == 'OK':
                    request.session.pop("Authority", None)
                    request.session.pop("Status", None)
                    order_verify_payment(order_transaction=order_transaction)
                else:
                    request.session.pop("Authority", None)
                    request.session.pop("Status", None)
                    order_transaction.status = OrderStatus.FAILED
                    order_transaction.save()
                    order_transaction.order.delete()

            return render(request, 'order_module/payment_verify.html',
                          {'order_transaction': order_transaction})
        else:
            raise Http404
