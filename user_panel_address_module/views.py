from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import ListView

from user_panel_address_module.context.create_or_update_address import create_or_update_address_context
from user_panel_address_module.context.enums import CreateOrUpdateAddressResult
from user_panel_address_module.forms import CreateOrUpdateAddressModelForm
from user_panel_address_module.model.address import Address
from user_panel_address_module.model.serializers.state_serializer import StateModelSerializer
from user_panel_address_module.model.state import State


# Create your views here.

@method_decorator(login_required, name='dispatch')
class AddressListView(ListView):
    model = Address
    template_name = 'user_panel_address_module/list.html'
    paginate_by = 6
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@login_required
def load_cities_view(request, state_id: int):
    if state_id:
        data = State.objects.filter(parent__isnull=False, parent_id=state_id)
        cities = StateModelSerializer(data, many=True)
        return JsonResponse({'cities': cities.data})
    raise Http404


@method_decorator(login_required, name='dispatch')
class CreateAddressView(View):
    def get(self, request):
        provinces = State.objects.filter(parent_id=None)
        next_url = request.GET.get('next', '')
        return render(request, 'user_panel_address_module/create.html',
                      {'form': CreateOrUpdateAddressModelForm(), 'provinces': provinces, 'next_url': next_url})

    def post(self, request):
        create_address_form = CreateOrUpdateAddressModelForm(request.POST)
        provinces = State.objects.filter(parent_id=None)
        next_url = request.POST.get('next')
        if create_address_form.is_valid():
            result = create_or_update_address_context(request, create_address_form, is_update=False)
            match result:
                case CreateOrUpdateAddressResult.success:
                    messages.success(request, CreateOrUpdateAddressResult.success.value)
                    # for validation host of next_url page
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect('user_panel_address_list_page')

                case CreateOrUpdateAddressResult.province_city_empty:
                    messages.error(request, CreateOrUpdateAddressResult.province_city_empty.value)
                    return render(request, 'user_panel_address_module/create.html',
                                  {'form': create_address_form, 'provinces': provinces, 'next_url': next_url})

                case CreateOrUpdateAddressResult.duplicated_phone_number:
                    create_address_form.add_error('phone_number',
                                                  CreateOrUpdateAddressResult.duplicated_phone_number.value)
                    return render(request, 'user_panel_address_module/create.html',
                                  {'form': create_address_form, 'provinces': provinces, 'next_url': next_url})

                case CreateOrUpdateAddressResult.not_valid:
                    messages.error(request, CreateOrUpdateAddressResult.not_valid.value)
                    return render(request, 'user_panel_address_module/create.html',
                                  {'form': create_address_form, 'provinces': provinces, 'next_url': next_url})

        return render(request, 'user_panel_address_module/create.html',
                      {'form': create_address_form, 'provinces': provinces, 'next_url': next_url})


@method_decorator(login_required, name='dispatch')
class UpdateAddressView(View):
    def get(self, request, address_id):

        address = get_object_or_404(Address, user_id=request.user.id, pk=address_id)
        provinces = State.objects.filter(parent__isnull=True).exclude(id=address.province.id)
        cities = State.objects.filter(parent__isnull=False, parent_id=address.province.id).exclude(id=address.city.id)

        return render(request, 'user_panel_address_module/edit.html',
                      {'form': CreateOrUpdateAddressModelForm(instance=address), 'address': address,
                       'provinces': provinces, 'cities': cities})

    def post(self, request, address_id):

        address = get_object_or_404(Address, user_id=request.user.id, pk=address_id)
        update_address_form = CreateOrUpdateAddressModelForm(request.POST, instance=address)
        provinces = State.objects.filter(parent__isnull=True).exclude(id=address.province.id)
        cities = State.objects.filter(parent__isnull=False, parent_id=address.province.id).exclude(id=address.city.id)

        if update_address_form.is_valid():
            result = create_or_update_address_context(request, update_address_form, is_update=True)
            match result:
                case CreateOrUpdateAddressResult.success:
                    messages.success(request, 'آدرس شما با موفقیت ویرایش شد !')
                    return redirect('user_panel_address_list_page')

                case CreateOrUpdateAddressResult.province_city_empty:
                    messages.error(request, CreateOrUpdateAddressResult.province_city_empty.value)
                    return render(request, 'user_panel_address_module/edit.html',
                                  {'form': update_address_form, 'address': address, 'provinces': provinces,
                                   'cities': cities})

                case CreateOrUpdateAddressResult.not_valid:
                    messages.error(request, CreateOrUpdateAddressResult.not_valid.value)
                    return render(request, 'user_panel_address_module/edit.html',
                                  {'form': update_address_form, 'address': address, 'provinces': provinces,
                                   'cities': cities})

        return render(request, 'user_panel_address_module/edit.html',
                      {'form': update_address_form, 'address': address, 'provinces': provinces, 'cities': cities})


def delete_address_view(request, address_id):
    if request.method == 'POST':
        address = get_object_or_404(Address, user_id=request.user.id, pk=address_id).delete()
        messages.success(request, 'آدرس مورد نظر شما با موفقیت حذف شد!')
        return redirect('user_panel_address_list_page')
    raise Http404


def activate_address_view(request, address_id):
    if request.method == 'POST':
        address = Address.objects.filter(user_id=request.user.id, is_active=True).first()
        if address:
            address.is_active = False
            address.save()

        new_address = Address.objects.filter(user_id=request.user.id, id=address_id, is_active=False).first()
        if new_address:
            new_address.is_active = True
            new_address.save()
            messages.success(request, 'آدرس مورد نظر شما با موفقیت فعال شد!')
            return redirect('user_panel_address_list_page')
        raise Http404

    raise Http404
