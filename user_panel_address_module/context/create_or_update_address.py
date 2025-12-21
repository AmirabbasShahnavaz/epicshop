from django.http import HttpRequest

from user_panel_address_module.context.enums import CreateOrUpdateAddressResult
from user_panel_address_module.forms import CreateOrUpdateAddressModelForm
from user_panel_address_module.model.address import Address
from user_panel_address_module.model.state import State


def create_or_update_address_context(request: HttpRequest,
                                     create_or_update_address_form: CreateOrUpdateAddressModelForm,
                                     is_update: bool):

    # region province_and_city_validations
    province = request.POST.get('province')
    city = request.POST.get('city')
    if not province or not city:
        return CreateOrUpdateAddressResult.province_city_empty

    province_data = State.objects.filter(parent__isnull=True, id=province).first()
    city_data = State.objects.filter(parent__isnull=False, id=city).first()
    if not province_data or not city_data:
        return CreateOrUpdateAddressResult.not_valid
    # endregion

    #region phone_number_validation
    phone_number = create_or_update_address_form.cleaned_data.get('phone_number')
    phone_number_exist = Address.objects.filter(phone_number__exact=phone_number).exclude(user=request.user).exists()
    if phone_number_exist:
        return CreateOrUpdateAddressResult.duplicated_phone_number
    #endregion

    street_or_neighborhood = create_or_update_address_form.cleaned_data.get('street_or_neighborhood')
    home_unit = create_or_update_address_form.cleaned_data.get('home_unit')
    plate_number = create_or_update_address_form.cleaned_data.get('plate_number')

    address = create_or_update_address_form.save(commit=False)

    if not is_update:
        # برای اینکه بفهمیم این کاربر اولین آدرسش هست یا نه
        address_model_exist = Address.objects.filter(user_id=request.user.id).exists()
        if not address_model_exist:
            address.is_active = True

    address.user_id = request.user.id
    address.province = province_data
    if home_unit:
        address.full_address = f'استان {province_data.title} - شهر {city_data.title} - محله/خ {street_or_neighborhood} - پلاک {plate_number} - واحد {home_unit}'
    else:
        address.full_address = f'استان {province_data.title} - شهر {city_data.title} - محله/خ {street_or_neighborhood} - پلاک {plate_number} - واحد '
    address.city = city_data
    address.save()

    return CreateOrUpdateAddressResult.success
