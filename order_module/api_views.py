from django.contrib import messages
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from helper_utils.basket import get_guest_id
from order_module.model import Basket, Order, OrderItem
from order_module.model.choices import OrderStatus


def get_user_or_guest_user_basket(request: HttpRequest, product_id: int, color_id: int):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user, product=product_id, product_color_id=color_id).first()
    # سشن کاربری که لاگین نکرده رو میگیریم یا اونو میسازیم چون الزامی هست
    guest_id = get_guest_id(request)
    return Basket.objects.filter(guest_id=guest_id, product=product_id, product_color_id=color_id).first()


class IncreaseBasketQuantityAPIView(APIView):
    def post(self, request: HttpRequest, product_id: int, color_id: int):
        basket = get_user_or_guest_user_basket(request, product_id, color_id)
        if basket:
            if basket.quantity < basket.product_color.quantity:
                basket.quantity += 1
                basket.save()
                return Response({'status': 'success'}, status=HTTP_200_OK)
            else:
                return Response({'status': 'quantity_limited', 'message': 'موجودی محصول به حداکثر رسید!'},
                                status=HTTP_200_OK)
        return Response({'status': 'basket_not_found', 'message': 'سبد خریدی یافت نشد!'},
                        status=HTTP_200_OK)


class DecreaseBasketQuantityAPIView(APIView):
    def post(self, request: HttpRequest, product_id: int, color_id: int):
        basket = get_user_or_guest_user_basket(request, product_id, color_id)
        if basket:
            if basket.quantity > 1:
                basket.quantity -= 1
                basket.save()
                return Response({'status': 'success'}, status=HTTP_200_OK)
            else:
                basket.delete()
                messages.success(request, 'محصول با موفقیت حذف شد !')
                return Response({'status': 'basket_removed'},
                                status=HTTP_200_OK)
        return Response({'status': 'basket_not_found', 'message': 'سبد خریدی یافت نشد!'},
                        status=HTTP_200_OK)


class DestroyBasketProductAPIView(APIView):
    def post(self, request: HttpRequest, product_id: int, color_id: int):
        basket = get_user_or_guest_user_basket(request, product_id, color_id)
        if basket:
            basket.delete()
            messages.success(request, 'محصول با موفقیت حذف شد !')
            return Response({'status': 'success'},
                            status=HTTP_200_OK)

        return Response({'status': 'basket_not_found', 'message': 'سبد خریدی یافت نشد!'},
                        status=HTTP_200_OK)