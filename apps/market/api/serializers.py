from apps.market import models
from rest_framework import serializers
from apps.media.api.serializers import MediaSerializer


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coin
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(CoinSerializer, self).to_representation(instance)


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chain
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(ChainSerializer, self).to_representation(instance)


class WalletTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WalletToken
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['media'] = MediaSerializer()
        return super(WalletTokenSerializer, self).to_representation(instance)


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['media'] = MediaSerializer()
        self.fields['chain'] = ChainSerializer()
        self.fields['coin'] = CoinSerializer()
        self.fields['collection'] = CollectionSerializer()
        self.fields['owner'] = WalletTokenSerializer()
        return super(AssetSerializer, self).to_representation(instance)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['media'] = MediaSerializer(many=True)
        return super(CollectionSerializer, self).to_representation(instance)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(FavoriteSerializer, self).to_representation(instance)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(ActivitySerializer, self).to_representation(instance)


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(PriceHistorySerializer, self).to_representation(instance)


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bid
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        return super(BidSerializer, self).to_representation(instance)