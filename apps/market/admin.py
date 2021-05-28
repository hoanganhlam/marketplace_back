from django.contrib import admin
from .models import Chain, Coin, Asset, WalletToken, Collection
# Register your models here.
admin.site.register((Chain, Coin, Asset, WalletToken, Collection))
