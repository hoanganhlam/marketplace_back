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
        self.fields['media'] = MediaSerializer()
        self.fields['logo'] = MediaSerializer()
        self.fields['banner'] = MediaSerializer()
        self.fields['owner'] = WalletTokenSerializer()
        return super(CollectionSerializer, self).to_representation(instance)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['fr'] = WalletTokenSerializer()
        self.fields['to'] = WalletTokenSerializer()
        self.fields['asset'] = AssetSerializer()
        return super(ActivitySerializer, self).to_representation(instance)


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Auction
        fields = '__all__'
        extra_fields = []
        extra_kwargs = {}

    def to_representation(self, instance):
        self.fields['coin'] = CoinSerializer()
        self.fields['fr'] = WalletTokenSerializer()
        self.fields['to'] = WalletTokenSerializer()
        self.fields['asset'] = AssetSerializer()
        self.fields['for_listing'] = AuctionSerializer()
        return super(AuctionSerializer, self).to_representation(instance)
