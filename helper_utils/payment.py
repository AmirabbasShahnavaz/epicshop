from utils.Config import Config
from zarinpal import ZarinPal

from order_module.model import OrderTransaction, OrderItem
from order_module.model.choices import OrderStatus
from user_panel_wallet_module.model import WalletTransaction
from user_panel_wallet_module.model.wallet import WalletStatus
from user_panel_wallet_module.model.wallet_transaction import WalletTransactionStatus

config = Config(
    merchant_id="23df5407-f30a-499e-ba8e-e7c90010a77f",
    sandbox=True  # موقع تست مقدار True | موقع انتشار مقدار False
)


# region wallet_payment
def wallet_payment_gateway(site_domain: str, wallet_transaction: WalletTransaction):
    try:
        zp = ZarinPal(config)
        payment = zp.payments.create({
            "amount": float(wallet_transaction.amount * 10),
            "description": "پرداخت سفارش #123",
            "callback_url": f'{site_domain}/user_panel/wallet/wallet_zarinpal_callback',
        })

        if payment['errors']:
            raise Exception(payment['errors'])

        authority = payment['data']['authority']
        wallet_transaction.authority = authority
        wallet_transaction.save()

        ipg_url = f'{zp.get_base_url()}/pg/StartPay/{authority}'
        return ipg_url

    except Exception as e:
        print(f"Erro of zarinpal payment : {e}")


def wallet_verify_payment(wallet_transaction: WalletTransaction):
    try:
        zp = ZarinPal(config)
        response = zp.verifications.verify({
            "merchant_id": config.merchant_id,
            "amount": float(wallet_transaction.amount * 10),
            "authority": wallet_transaction.authority,
        })

        if response.get('data') and response['data'].get('code', 0) >= 100:
            wallet_transaction.ref_id = response['data'].get('ref_id')
            wallet_transaction.code = response['data'].get('code')
            wallet_transaction.message = response['data'].get('message')
            wallet_transaction.card_hash = response['data'].get('card_hash')
            wallet_transaction.card_pan = response['data'].get('card_pan')
            wallet_transaction.status = WalletTransactionStatus.PAID
            wallet_transaction.wallet.status = WalletStatus.Deposit
            wallet_transaction.wallet.save()

        else:
            wallet_transaction.status = WalletTransactionStatus.FAILED
            wallet_transaction.wallet.delete()

        wallet_transaction.save()
        return wallet_transaction


    except Exception as e:
        print(f"Erro of zarinpal payment : {e}")


# endregion

# region order_payment
def order_payment_gateway(site_domain: str, order_transaction: OrderTransaction):
    try:

        zp = ZarinPal(config)
        payment = zp.payments.create({
            "amount": float(order_transaction.amount * 10),
            "description": "پرداخت سفارش #123",
            "callback_url": f'{site_domain}/order/zarinpal_callback',
        })

        if payment['errors']:
            raise Exception(payment['errors'])

        authority = payment['data']['authority']
        order_transaction.authority = authority
        order_transaction.save()

        ipg_url = f'{zp.get_base_url()}/pg/StartPay/{authority}'
        return ipg_url

    except Exception as e:
        print(f"Erro of zarinpal payment : {e}")


def order_verify_payment(order_transaction: OrderTransaction):
    try:
        zp = ZarinPal(config)
        response = zp.verifications.verify({
            "merchant_id": config.merchant_id,
            "amount": float(order_transaction.amount * 10),
            "authority": order_transaction.authority,
        })

        if response.get('data') and response['data'].get('code', 0) >= 100:
            order_transaction.ref_id = response['data'].get('ref_id')
            order_transaction.code = response['data'].get('code')
            order_transaction.message = response['data'].get('message')
            order_transaction.card_hash = response['data'].get('card_hash')
            order_transaction.card_pan = response['data'].get('card_pan')
            order_transaction.status = OrderStatus.PAID
            order_transaction.order.status = OrderStatus.PAID
            order_items = OrderItem.objects.filter(order=order_transaction.order)
            for order_item in order_items:
                order_item.product_color.quantity -= order_item.quantity
                order_item.product_color.save()

            order_transaction.order.save()

        else:
            order_transaction.status = WalletTransactionStatus.FAILED
            order_transaction.order.delete()

        order_transaction.save()
        return order_transaction


    except Exception as e:
        print(f"Erro of zarinpal payment : {e}")
# endregion
