from django.db.models import When, Case, Sum, DecimalField, F

from user_panel_wallet_module.model import Wallet
from user_panel_wallet_module.model.wallet import WalletStatus


def get_all_wallet_balance_amount(user_id):
    return Wallet.objects.filter(
        user_id=user_id
    ).exclude(
        status=WalletStatus.Pending
    ).aggregate(
        balance=Sum(
            Case(
                When(status=WalletStatus.Deposit, then=F('amount')),
                When(status=WalletStatus.Creditor, then=-F('amount')),
                output_field=DecimalField()
            )
        )
    )['balance'] or 0