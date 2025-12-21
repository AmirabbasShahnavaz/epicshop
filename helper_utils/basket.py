from django.http import HttpRequest


def get_guest_id(request: HttpRequest):
    guest_id = request.session.session_key
    if guest_id is None:
        request.session.create()
        guest_id = request.session.session_key
    return guest_id


def get_all_total_price(basket_items):
    total_price = 0
    for basket_item in basket_items:
        total_price += basket_item.get_total_price()
    return total_price




def get_pay_amount(order_amount):
    tax_price = (order_amount * 10) / 100
    return int(order_amount + tax_price)


def get_tax_amount(order_amount):
    return (order_amount * 10) / 100
