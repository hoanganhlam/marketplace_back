from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'wallets', views.WalletTokenViewSet)
router.register(r'assets', views.AssetViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'auctions', views.AuctionViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'chains', views.ChainViewSet)
router.register(r'activities', views.ActivityViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^featured/$', views.featured),
    url(r'^price-history/$', views.price_history),
    url(r'^good-listing/$', views.good_listing),
    url(r'^sync-wallet/(?P<wallet_address>[-\w]+)/$', views.sync_wallet),
]
