from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base import pagination
from . import serializers
from apps.market import models
from django.db.models import Q


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
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


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
    queryset = models.objects.order_by('-id').select_related("coin").select_related("chain").select_related("collection")
    serializer_class = serializers.AssetSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


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
    filter_backends = [OrderingFilter]
    lookup_field = 'slug'


class PriceHistoryViewSet(viewsets.ModelViewSet):
    models = models.PriceHistory
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.PriceHistorySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


class BidViewSet(viewsets.ModelViewSet):
    models = models.Bid
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.BidSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


class ActivityViewSet(viewsets.ModelViewSet):
    models = models.Activity
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.ActivitySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'


@api_view(['GET'])
def featured(request):
    item = models.Asset.objects.order_by("?").first()
    return Response(serializers.AssetSerializer(item).data)
