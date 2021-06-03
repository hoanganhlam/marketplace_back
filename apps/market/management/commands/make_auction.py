from django.core.management.base import BaseCommand
from apps.market.models import Asset, Auction, WalletToken, Coin
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        wallet_a = WalletToken.objects.get(pk=1)
        wallet_b = WalletToken.objects.get(pk=2)
        assets = list(Asset.objects.all())
        for asset in assets:
            coin = Coin.objects.order_by("?").first()
            d = datetime.now()
            auction_listing = Auction.objects.create(
                fr=wallet_a,
                is_listing=True,
                coin=coin,
                asset=asset,
                expired=d + timedelta(days=30),
                unit_price=random.randrange(1, 10),
                quantity=random.randrange(2, 6)
            )
            auction_offer = Auction.objects.create(
                fr=wallet_a,
                coin=coin,
                asset=asset,
                expired=d + timedelta(days=15),
                unit_price=random.randrange(1, 10),
                quantity=random.randrange(2, 6)
            )
            auction_listing.to = wallet_b
            auction_listing.is_complete = True
            auction_listing.save()
            auction_offer.to = wallet_b
            auction_offer.is_complete = True
            auction_offer.save()
