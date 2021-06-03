from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Auction, Activity


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
    else:
        if instance.is_complete:
            for e in ["AUCTION_SUCCESSFUL", "ASSET_TRANSFER"]:
                Activity.objects.create(
                    event=e,
                    fr=instance.fr,
                    to=instance.to,
                    asset=instance.asset,
                    quantity=instance.quantity,
                    unit_price=instance.unit_price
                )
