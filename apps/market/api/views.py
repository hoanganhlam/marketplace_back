from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base import pagination
from . import serializers
from apps.market import models
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone


class WalletTokenViewSet(viewsets.ModelViewSet):
    models = models.WalletToken
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.WalletTokenSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['full_name']
    lookup_field = 'address'


class CoinViewSet(viewsets.ModelViewSet):
    models = models.Coin
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.CoinSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title']
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        q = Q()
        if request.GET.get("primary") and request.GET.get("primary") == "true":
            q = q & Q(primary=True)
        queryset = self.filter_queryset(models.Coin.objects.filter(q).order_by('-id').distinct())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChainViewSet(viewsets.ModelViewSet):
    models = models.Chain
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.ChainSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


class AssetViewSet(viewsets.ModelViewSet):
    models = models.Asset
    queryset = models.objects.order_by('-id') \
        .select_related("coin") \
        .select_related("chain") \
        .select_related("collection")
    serializer_class = serializers.AssetSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        # models.Asset.objects.filter(-)
        q = Q()
        # statuses
        if request.GET.get("statuses"):
            q = q & Q(status__in=request.GET.get("statuses").split(","))
        # collections
        if request.GET.get("collections"):
            arr = request.GET.get("collections").split(",")
            q = q & (Q(collection__id__in=arr) | Q(collection__related__id__in=arr))
        # chains
        if request.GET.get("chains"):
            q = q & Q(chain__in=request.GET.get("chains").split(","))
        # coins
        if request.GET.get("coins"):
            q = q & Q(coin__in=request.GET.get("coins").split(","))
        # max, min,
        if request.GET.get("max"):
            q = q & Q(price__lte=float(request.GET.get("max")))
        if request.GET.get("min"):
            q = q & Q(price__gte=float(request.GET.get("min")))
        # favor
        if request.GET.get("favor"):
            q = q & Q(favorites__owner__address=request.GET.get("favor"))
        # owner
        if request.GET.get("owner"):
            q = q & Q(owner__address=request.GET.get("owner"))
        # order

        queryset = self.filter_queryset(
            models.Asset.objects
                .order_by('-id')
                .select_related("coin")
                .select_related("chain")
                .select_related("collection")
                .filter(q)
                .distinct()
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    models = models.Favorite
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.FavoriteSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


class CollectionViewSet(viewsets.ModelViewSet):
    models = models.Collection
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.CollectionSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title']
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        q = Q()
        if request.GET.get("primary") and request.GET.get("primary") == "true":
            q = q & Q(primary=True)
        else:
            q = q & ~Q(primary=True)
        queryset = self.filter_queryset(models.Collection.objects.filter(q).order_by('-id').distinct())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AuctionViewSet(viewsets.ModelViewSet):
    models = models.Auction
    queryset = models.objects.order_by('-id') \
        .select_related("coin") \
        .select_related("fr") \
        .select_related("to") \
        .select_related("asset")
    serializer_class = serializers.AuctionSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        q = Q()
        # is_listing
        q = q & Q(is_listing=request.GET.get("is_listing") == "true")
        # from
        if request.GET.get("fr"):
            q = q & Q(fr__address=request.GET.get("fr"))
        # asset
        if request.GET.get("asset"):
            q = q & Q(asset__id=request.GET.get("asset"))
        queryset = self.filter_queryset(
            models.Auction.objects.order_by('-id')
                .select_related("coin")
                .select_related("fr")
                .select_related("to")
                .select_related("asset")
                .filter(q)
                .distinct()
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    models = models.Activity
    queryset = models.objects.order_by('-id') \
        .select_related("fr") \
        .select_related("to") \
        .select_related("asset")
    serializer_class = serializers.ActivitySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        q = Q()
        # events
        if request.GET.get("events"):
            q = q & Q(event__in=request.GET.get("events").split(","))
        # from
        if request.GET.get("fr"):
            q = q & Q(fr__address=request.GET.get("fr"))
        # asset
        if request.GET.get("asset"):
            q = q & Q(asset__id=request.GET.get("asset"))

        # chains
        if request.GET.get("chains"):
            arr = request.GET.get("chains").split(",")
            q = q & Q(asset__chain__id__in=arr)
        # collections
        if request.GET.get("collections"):
            arr = request.GET.get("collections").split(",")
            q = q & (Q(asset__collection__id__in=arr) | Q(asset__collection__related__id__in=arr))
        queryset = self.filter_queryset(
            models.Activity.objects.order_by('-id').select_related("fr").select_related("to").select_related(
                "asset").filter(q).distinct()
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def featured(request):
    item = models.Asset.objects.order_by("?").first()
    return Response(serializers.AssetSerializer(item).data)


@api_view(['GET'])
def price_history(request):
    asset_address = request.GET.get("asset")
    now = timezone.now()
    rg = request.GET.get("range", "7")
    start = now - timedelta(days=int(rg))
    queryset = models.Auction.objects\
        .only("updated", "unit_price")\
        .filter(asset__id=asset_address, updated__range=[str(start), str(now)])
    out = list(map(lambda x: {
        "price": x.unit_price,
        "date": x.updated
    }, queryset))
    return Response(out)


@api_view(['GET'])
def good_listing(request):
    asset_address = request.GET.get("asset")
    q = Q(is_listing=True, asset__id=asset_address)
    q = q & (Q(expired__gt=timezone.now()) | Q(expired__isnull=True))
    listing = models.Auction.objects.filter(q).order_by("unit_price").first()
    return Response(serializers.AuctionSerializer(listing).data)
