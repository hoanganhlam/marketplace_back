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
    permission_classes = permissions.IsAuthenticatedOrReadOnly,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['full_name']
    lookup_field = 'address'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoinViewSet(viewsets.ModelViewSet):
    models = models.Coin
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.CoinSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChainViewSet(viewsets.ModelViewSet):
    models = models.Chain
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.ChainSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        q = Q(db_status=1)
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        q = Q(db_status=1)
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuctionViewSet(viewsets.ModelViewSet):
    models = models.Auction
    queryset = models.objects.order_by('-id') \
        .select_related("coin") \
        .select_related("fr") \
        .select_related("to") \
        .select_related("asset") \
        .select_related("for_listing")
    serializer_class = serializers.AuctionSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        q = Q(db_status=1)
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
                .select_related("for_listing")
                .filter(q)
                .distinct()
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        q = Q(db_status=1)
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.db_status = -1
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    queryset = models.Auction.objects \
        .only("updated", "unit_price") \
        .filter(asset__id=asset_address, updated__range=[str(start), str(now)])
    out = list(map(lambda x: {
        "price": x.unit_price,
        "date": x.updated
    }, queryset))
    return Response(out)


@api_view(['GET'])
def good_listing(request):
    asset_address = request.GET.get("asset")
    asset = models.Asset.objects.get(pk=asset_address)
    q = Q(is_listing=True, asset__id=asset_address, db_status=1, quantity__gt=0)
    q = q & (Q(expired__gt=timezone.now()) | Q(expired__isnull=True))
    listing = models.Auction.objects.filter(q).order_by("unit_price").first()
    if listing and asset.price != listing.unit_price:
        asset.price = listing.unit_price
        asset.save()
    return Response(serializers.AuctionSerializer(listing).data)


@api_view(['GET'])
def sync_wallet(request, wallet_address):
    item, is_created = models.WalletToken.objects.get_or_create(address=wallet_address)
    return Response(serializers.WalletTokenSerializer(item).data)


@api_view(['GET', 'POST'])
def save_asset(request, pk):
    asset = models.Asset.objects.get(pk=pk)
    owner = models.WalletToken.objects.get(address=request.GET.get("owner"))
    if request.method == "GET":
        dataset = asset.hearts.all()
        return Response({
            "is_saved": owner in dataset,
            "total": len(dataset)
        })
    else:
        if owner in asset.hearts.all():
            asset.hearts.remove(owner)
            flag = False
        else:
            asset.hearts.add(owner)
            flag = True
        return Response({
            "is_saved": flag,
            "total": len(asset.hearts.all())
        })
