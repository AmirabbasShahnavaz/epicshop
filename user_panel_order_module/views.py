from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.db.models.aggregates import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from helper_utils.basket import get_tax_amount
from order_module.model import Order
from order_module.model.choices import OrderStatus


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'user_panel_order_module/order_list.html'
    paginate_by = 1

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status') or OrderStatus.PAID
        page_number = self.request.GET.get('page') or 1
        context['current_page'] = int(page_number)
        stats = Order.objects.filter(user=self.request.user).exclude(status=OrderStatus.PENDING).aggregate(
            canceled_count=Count('id', filter=Q(status=OrderStatus.CANCELED)),
            paid_count=Count('id', filter=Q(status=OrderStatus.PAID))
        )

        context['paid_count'] = stats['paid_count']
        context['canceled_count'] = stats['canceled_count']

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user).prefetch_related('orders').exclude(
            status=OrderStatus.PENDING).order_by(
            '-created_at')
        order_status = self.request.GET.get('status') or OrderStatus.PAID
        queryset = queryset.filter(status=order_status)

        return queryset


class OrderDetailsView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'user_panel_order_module/order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tax_price'] = get_tax_amount(self.object.amount)
        print(get_tax_amount(self.object.amount))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, status=OrderStatus.PAID).prefetch_related('orders')
