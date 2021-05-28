from django.db import models
from django.contrib.auth.models import User
from base.interface import BaseModel, Taxonomy
from apps.media.models import Media
from django.db.models import JSONField
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class WalletToken(BaseModel):
    address = models.CharField(max_length=120)
    media = models.ForeignKey(Media, related_name="wallet", null=True, blank=True, on_delete=models.SET_NULL)
    banner = models.ForeignKey(Media, related_name="banner_wallet", null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(null=True, blank=True, max_length=120)
    bio = models.CharField(null=True, blank=True, max_length=240)
    meta = JSONField(null=True, blank=True)


class Coin(BaseModel, Taxonomy):
    code = models.CharField(max_length=120)
    media = models.ForeignKey(Media, related_name="coins", null=True, blank=True, on_delete=models.SET_NULL)


class Chain(BaseModel, Taxonomy):
    code = models.CharField(max_length=120)
    media = models.ForeignKey(Media, related_name="chains", null=True, blank=True, on_delete=models.SET_NULL)


class Collection(Taxonomy, BaseModel):
    description = models.TextField(max_length=1000, null=True, blank=True)
    media = models.ForeignKey(Media, related_name="collections", null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(WalletToken, related_name="collections", on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)
    meta = JSONField(null=True, blank=True)
    related = models.ManyToManyField("self", related_name="related_reverse", blank=True)


class Asset(Taxonomy, BaseModel):
    title = models.CharField(max_length=120)
    token = models.CharField(max_length=120, null=True, blank=True)
    contract = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    STATUS_CHOICE = (
        ("BUY_NOW", _("BUY_NOW")),
        ("ON_AUCTION", _("ON_AUCTION")),
        ("IS_NEW", _("IS_NEW")),
        ("HAS_OFFERS", _("HAS_OFFERS")),
    )

    status = models.CharField(choices=STATUS_CHOICE, default="IS_NEW", max_length=50)
    price = models.FloatField(default=0)
    collection = models.ForeignKey(Collection, related_name="assets", on_delete=models.CASCADE, null=True, blank=True)
    chain = models.ForeignKey(Chain, related_name="assets", on_delete=models.CASCADE, null=True, blank=True)
    coin = models.ForeignKey(Coin, related_name="assets", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(WalletToken, related_name="assets", on_delete=models.CASCADE)
    hearts = models.ManyToManyField(WalletToken, related_name="hearted_assets", blank=True)
    media = models.ForeignKey(Media, related_name="assets", null=True, blank=True, on_delete=models.SET_NULL)
    meta = JSONField(null=True, blank=True)


class Favorite(BaseModel):
    owner = models.ForeignKey(WalletToken, related_name="favorites", on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, related_name="favorites", on_delete=models.CASCADE)


class Activity(BaseModel):
    fr = models.ForeignKey(WalletToken, on_delete=models.CASCADE, related_name="fr_activities")
    asset = models.ForeignKey(Asset, related_name="fr_activities", on_delete=models.CASCADE)
    to = models.ForeignKey(WalletToken, on_delete=models.CASCADE, related_name="to_activities")
    EVENT_CHOICE = (
        ("AUCTION_CREATED", _("AUCTION_CREATED")),
        ("OFFER_ENTERED", _("OFFER_ENTERED")),
        ("ASSET_TRANSFER", _("ASSET_TRANSFER")),
        ("AUCTION_SUCCESSFUL", _("AUCTION_SUCCESSFUL")),
    )
    event = models.CharField(choices=EVENT_CHOICE, default="AUCTION_SUCCESSFUL", max_length=50)
    unit_price = models.BooleanField(default=0)
    quantity = models.IntegerField(default=1)


class PriceHistory(BaseModel):
    asset = models.ForeignKey(Asset, related_name="price_histories", on_delete=models.CASCADE)
    price = models.FloatField(default=0)


class Bid(BaseModel):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="bids")
    owner = models.ForeignKey(WalletToken, on_delete=models.CASCADE, related_name="bids")
    asset = models.ForeignKey(Asset, related_name="bids", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    expired = models.DateTimeField()
