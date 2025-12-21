from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from helper_utils.payment import wallet_payment_gateway, wallet_verify_payment
from helper_utils.wallet import get_all_wallet_balance_amount
from user_panel_wallet_module.forms import WalletChargingForm
from user_panel_wallet_module.model import WalletTransaction, Wallet
from user_panel_wallet_module.model.wallet_transaction import WalletTransactionStatus


# Create your views here.

@method_decorator(login_required, name='dispatch')
class WalletListView(ListView):
    model = Wallet
    template_name = 'user_panel_wallet_module/wallet.html'
    context_object_name = 'wallet_list'
    paginate_by = 6

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page')

        try:
            page_number = int(page)
        except (TypeError, ValueError):
            page_number = 1

        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return paginator, page_obj, page_obj.object_list, True

    def get_queryset(self, **kwargs):
        query = super(WalletListView, self).get_queryset()
        query = query.filter(user=self.request.user)
        return query

    def get_context_data(self, **kwargs):
        context = super(WalletListView, self).get_context_data(**kwargs)
        context['form'] = WalletChargingForm()
        context['paging_background'] = True
        context['total_wallet_balance_amount'] = get_all_wallet_balance_amount(self.request.user.id)
        page_number = self.request.GET.get('page') or 1
        context['current_page'] = int(page_number)
        return context

    def post(self, request):
        wallet_list = self.get_queryset()
        wallet_charging_form = WalletChargingForm(request.POST)
        if wallet_charging_form.is_valid():
            amount = wallet_charging_form.cleaned_data.get('amount')

            new_wallet = Wallet.objects.create(user_id=request.user.id, description='شارژ کیف پول', amount=amount)
            new_wallet.save()

            new_wallet_transaction = WalletTransaction.objects.create(wallet_id=new_wallet.id, amount=amount)
            new_wallet_transaction.save()

            ipg_url = wallet_payment_gateway(site_domain=settings.SITE_DOMAIN,
                                             wallet_transaction=new_wallet_transaction)
            if ipg_url is None:
                new_wallet.delete()
                new_wallet_transaction.delete()
                messages.error(request, 'خطا در ارسال به درگاه')
                return redirect('user_panel_wallet_index_page')

            return redirect(ipg_url)

        return render(request, 'user_panel_wallet_module/wallet.html',
                      {'form': wallet_charging_form, 'wallet_list': wallet_list})


def wallet_zarinpal_callback(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if authority != '' and status != '':
        request.session["Authority"] = authority
        request.session["Status"] = status
        return redirect('user_panel_wallet_verify_page')


class WalletVerifyView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        authority = request.session.get('Authority')
        status = request.session.get('Status')
        if authority is not None and status is not None:
            wallet_transaction = WalletTransaction.objects.filter(authority__exact=authority).first()
            if not wallet_transaction:
                request.session.pop("Authority", None)
                request.session.pop("Status", None)
                raise Http404

            if wallet_transaction.status == WalletTransactionStatus.PENDING:
                if status == 'OK':
                    request.session.pop("Authority", None)
                    request.session.pop("Status", None)
                    wallet_verify_payment(wallet_transaction=wallet_transaction)
                else:
                    wallet_transaction.status = WalletTransactionStatus.FAILED
                    wallet_transaction.save()
                    wallet_transaction.wallet.delete()

            return render(request, 'user_panel_wallet_module/payment_verify.html',
                          {'wallet_transaction': wallet_transaction})
        else:
            raise Http404