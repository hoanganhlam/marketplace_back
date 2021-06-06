from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.market.models import Auction, Asset, WalletToken, Collection, Activity


@receiver(post_save, sender=Auction)
def on_post_save(sender, instance, created, *args, **kwargs):
    # AUCTION_CREATED - OFFER_ENTERED - ASSET_TRANSFER - AUCTION_SUCCESSFUL
    if created:
        if instance.is_listing:
            e = "AUCTION_CREATED"
        else:
            e = "OFFER_ENTERED"
        Activity.objects.create(
            event=e,
            fr=instance.fr,
            to=instance.to,
            asset=instance.asset,
            quantity=instance.quantity,
            unit_price=instance.unit_price,
        )
