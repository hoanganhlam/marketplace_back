from django.core.management.base import BaseCommand
from apps.media.models import Media
from apps.market.models import Coin, Chain, WalletToken, Asset, Collection
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        for own in ["0x9aF493BC3deFCe2933E8f08B4dB8E4BfD63e25b4", "0x9aF493BC3deFCe2933E8f08B4dB8E4BfD63e25b6"]:
            WalletToken.objects.get_or_create(address=own)
        with open('apps/market/seed/chains.json') as chain_file:
            chains = json.load(chain_file)
            for ch in chains:
                Chain.objects.get_or_create(title=ch.get("title"), defaults={
                    "code": ch.get("title")
                })
        with open('apps/market/seed/coins.json') as coin_file:
            coins = json.load(coin_file)
            for co in coins:
                Coin.objects.get_or_create(title=co.get("title"), defaults={
                    "code": co.get("title")
                })
        with open('apps/market/seed/assets.json') as asset_file:
            collections = json.load(asset_file)
            for coll in collections:
                if coll.get("owner") is None:
                    coll["owner"] = "0x9aF493BC3deFCe2933E8f08B4dB8E4BfD63e25b4"
                owner, created = WalletToken.objects.get_or_create(address=coll["owner"])
                collection_instance, created = Collection.objects.get_or_create(
                    title=coll.get("title"),
                    defaults={
                        "description": coll.get("desc"),
                        "owner": owner,
                        "primary": coll.get("assets") is None or len(coll.get("assets")) == 0
                    }
                )
                if not coll.get("assets"):
                    coll["assets"] = []
                for asset in coll.get("assets"):
                    if asset.get("owner") is None:
                        asset["owner"] = "0x9aF493BC3deFCe2933E8f08B4dB8E4BfD63e25b4"
                    owner, created = WalletToken.objects.get_or_create(address=asset["owner"])
                    chain, created = Chain.objects.get_or_create(title=asset.get("chain"))
                    coin, created = Coin.objects.get_or_create(title=asset.get("coin"))
                    media = None
                    if asset.get("media"):
                        media = Media.objects.save_url(asset.get("media"))
                    asset_instance, created = Asset.objects.get_or_create(
                        title=asset.get("title"),
                        defaults={
                            "description": asset.get("desc"),
                            "token": asset.get("token"),
                            "contract": asset.get("contract"),
                            "media": media,
                            "price": float(asset.get("price")),
                            "owner": owner,
                            "chain": chain,
                            "coin": coin,
                            "collection": collection_instance
                        },
                    )
                    if not created:
                        asset_instance.media = media
                        asset_instance.save()
