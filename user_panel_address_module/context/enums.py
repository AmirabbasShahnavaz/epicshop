import enum


class CreateOrUpdateAddressResult(enum.Enum):
    success = 'آدرس جدید شما با موفقیت افزوده شد!'
    update_success = 'آدرس مورد نظر شما با موفقیت ویرایش شد!'
    province_city_empty = 'لطفا استان و شهر خود را وارد کنید!'
    not_valid = 'لطفا استان و شهر درستی را انتخاب کنید!'
    duplicated_phone_number = 'تلفن همراه وارد شده قبلا ثبت شده است'