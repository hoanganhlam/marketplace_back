from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'wallets', views.WalletTokenViewSet)
router.register(r'assets', views.AssetViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'bids', views.BidViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'chains', views.ChainViewSet)
router.register(r'activities', views.ActivityViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^featured/$', views.featured),
]
