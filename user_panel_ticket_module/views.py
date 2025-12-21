from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from authentication_module.model import User
from user_panel_ticket_module.context.create_ticket import create_ticket_context, CreateTicketResult
from user_panel_ticket_module.forms import SendTicketMessageForm, CreateTicketForm
from user_panel_ticket_module.model import Ticket, TicketMessage
from user_panel_ticket_module.model.choices import TicketStatus


# Create your views here.
class TicketCreateView(View):
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login_page')

        user: User = get_object_or_404(User, id=request.user.id)
        if not user.first_name:
            messages.error(request, 'برای ساخت تیکت جدید ابتدا باید حساب کاربری خود را تکمیل تر کنید!')
            return JsonResponse({'status': 'no_complete',
                                 'url': f'{reverse('user_panel_edit_user_page')}?next={reverse('user_panel_ticket_list_page')}'},
                                safe=False)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        view = render_to_string('user_panel_ticket_module/includes/ticket_create.html',
                                {'form': CreateTicketForm(), 'message_form': SendTicketMessageForm()}, request)
        return JsonResponse(view, safe=False)

    def post(self, request):
        create_ticket_form = CreateTicketForm(request.POST)

        message_form = SendTicketMessageForm(request.POST)
        if create_ticket_form.is_valid() and message_form.is_valid():

            result = create_ticket_context(request, create_ticket_form, message_form)
            match result:
                case CreateTicketResult.success:
                    return JsonResponse({'status': 'success',
                                         'message': 'تیکت شما با موفقیت ثبت شد و در اسرع وقت تیم پشتیبانی به تیکت شما پاسخ میدن !'},
                                        safe=False)
                case CreateTicketResult.error:
                    return JsonResponse({'status': 'error',
                                         'message': 'شما نمیتوانید بیشتر از 3 تیکت درحال بررسی داشته باشید!'},
                                        safe=False)
        print('mosdkawpdolkefok')
        html = render_to_string('user_panel_ticket_module/includes/ticket_create.html', {
            'form': create_ticket_form,
            'message_form': message_form
        }, request)
        return JsonResponse({'status': 'is_not_valid', 'html': html}, safe=False)


@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = 'user_panel_ticket_module/ticket_list.html'
    paginate_by = 6

    # region pagination
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

    # endregion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Ticket.objects.filter(user=self.request.user).aggregate(
            closed_count=Count('id', filter=Q(status=TicketStatus.Closed)),
            pending_count=Count('id', filter=Q(Q(status=TicketStatus.Pending) | Q(status=TicketStatus.AnsweredByUser))),
            answered_count=Count('id', filter=Q(status=TicketStatus.AnsweredByAdmin)),
            all_count=Count('id'),
        )

        context['current_page'] = self.request.GET.get('page') or 1
        context['sort_by'] = self.request.GET.get('sort_by') or ''
        context['search'] = self.request.GET.get('q') or ''
        context['closed_count'] = stats['closed_count']
        context['pending_count'] = stats['pending_count']
        context['answered_count'] = stats['answered_count']
        context['all_count'] = stats['all_count']
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(title__icontains=search)

        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            match sort_by:
                case 'pending':
                    queryset = queryset.filter(Q(status__exact='Pending') | Q(status__exact='AnsweredByUser'))
                case 'answered':
                    queryset = queryset.filter(status__exact='AnsweredByAdmin')
                case 'closed':
                    queryset = queryset.filter(status__exact='Closed')

        return queryset


@method_decorator(login_required, name='dispatch')
class TicketDetailsView(View):
    def get(self, request: HttpRequest, ticket_code):
        user_ticket = Ticket.objects.filter(user=self.request.user, ticket_code__exact=ticket_code).prefetch_related(
            'messages').first()
        if not user_ticket:
            raise Http404

        return render(request, 'user_panel_ticket_module/ticket_details.html',
                      {'ticket': user_ticket, 'form': SendTicketMessageForm()})

    def post(self, request: HttpRequest):
        ticket_code = request.POST.get('ticket_code')
        user_ticket = get_object_or_404(Ticket, user=self.request.user, ticket_code__exact=ticket_code)

        send_message_form = SendTicketMessageForm(request.POST)
        if send_message_form.is_valid():
            new_ticket_message = TicketMessage(user=request.user, ticket=user_ticket,
                                               message=send_message_form.cleaned_data.get('message'))
            new_ticket_message.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('user_panel_ticket_details_page')

        return render(request, 'user_panel_ticket_module/ticket_details.html', {'form': send_message_form})


@method_decorator(login_required, name='dispatch')
class CancelTicketView(View):
    def post(self, request: HttpRequest):
        ticket_code = request.POST.get('ticket_code')
        user_ticket = get_object_or_404(Ticket, user=self.request.user, ticket_code__exact=ticket_code)
        user_ticket.status = TicketStatus.Closed
        user_ticket.save()
        messages.success(request, f'تیک {ticket_code}# با موفقیت بسته شد!')
        return redirect('user_panel_ticket_details_page', ticket_code=ticket_code)
