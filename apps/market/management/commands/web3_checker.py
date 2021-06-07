from django.core.management.base import BaseCommand
from web3 import Web3
import time
import json
import threading
import math
from apps.market.models import Auction, Asset, WalletToken, Collection, Activity
from datetime import timedelta
from django.utils import timezone

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))
with open("contract_abi.json") as f:
    info_json = json.load(f)
abi = info_json
contractAddress = '0xFAfb3b04fe227f4871efA3269f0d3292CFF5646d'
contract = w3.eth.contract(address=contractAddress, abi=abi)
block_filter = w3.eth.filter({'fromBlock': 'latest', 'address': contractAddress})


def handle_event(event):
    print(event)
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = contract.events.List().processReceipt(receipt)
    flag = "listing"
    if len(result) == 0:
        result = contract.events.Buy().processReceipt(receipt)
        flag = "buy"
    if len(result) == 0:
        result = contract.events.CreateOffer().processReceipt(receipt)
        flag = "create_offer"
    if len(result) == 0:
        result = contract.events.AcceptOffer().processReceipt(receipt)
        flag = "accept_offer"
    if len(result) == 0:
        result = contract.events.CancelList().processReceipt(receipt)
        flag = "cancel_list"
    if len(result) == 0:
        return
    raw_data = json.loads(Web3.toJSON(result[0]['args']))
    fr, created = WalletToken.objects.get_or_create(address=raw_data.get("from"))
    now = timezone.now()
    expired = now + timedelta(days=7)
    print(raw_data)
    print(flag)
    if flag == "listing":
        checker = Auction.objects.filter(bc_listing_id=raw_data.get("itemId")).first()
        if checker is None:
            ct, created = Collection.objects.get_or_create(
                token=raw_data.get("tokenAddress"),
                defaults={
                    "owner": fr
                }
            )
            asset, created = Asset.objects.get_or_create(
                contract=raw_data.get("tokenAddress"),
                token=raw_data.get("tokenId"),
                defaults={
                    "collection": ct,
                    "owner": fr
                }
            )
            Auction.objects.create(
                bc_listing_id=raw_data.get("itemId"),
                unit_price=raw_data.get("pricePerToken") / math.pow(10, 18),
                quantity=raw_data.get("tokenAmount"),
                fr=fr,
                asset=asset,
                expired=expired,
                is_listing=True
            )
    elif flag == "create_offer":
        if raw_data.get("itemId"):
            listing = Auction.objects.filter(is_listing=True, bc_listing_id=raw_data.get("itemId")).first()
            if listing:
                Auction.objects.create(
                    bc_listing_id=raw_data.get("itemId"),
                    bc_offer_id=raw_data.get("offerId"),
                    unit_price=raw_data.get("paymentAmount") / math.pow(10, 18),
                    quantity=raw_data.get("itemAmount"),
                    fr=fr,
                    to=listing.fr,
                    asset=listing.asset,
                    expired=expired,
                    is_listing=False,
                    for_listing=listing
                )
    elif flag == "accept_offer":
        listing = Auction.objects.filter(bc_listing_id=raw_data.get("itemId")).first()
        offer = Auction.objects.filter(bc_offer_id=raw_data.get("offerId")).first()
        if listing and offer:
            quantity = offer.quantity
            listing.quantity = listing.quantity - quantity
            listing.is_complete = True
            if listing.quantity <= 0:
                listing.db_status = -1
            listing.save()
            offer.db_status = -1
            Activity.objects.create(
                event="AUCTION_SUCCESSFUL",
                fr=offer.fr,
                to=offer.to,
                asset=listing.asset,
                quantity=quantity,
                unit_price=offer.unit_price
            )
    elif flag == "buy":
        quantity = raw_data.get("itemAmount")
        listing = Auction.objects.filter(bc_listing_id=raw_data.get("itemId")).first()
        if listing:
            listing.quantity = listing.quantity - quantity
            if listing.quantity <= 0:
                listing.db_status = -1
            listing.is_complete = True
            listing.save()
            if fr:
                Activity.objects.create(
                    event="AUCTION_SUCCESSFUL",
                    fr=listing.fr,
                    to=fr,
                    asset=listing.asset,
                    quantity=quantity,
                    unit_price=listing.unit_price
                )
    elif flag == "cancel_list":
        listing = Auction.objects.filter(bc_listing_id=raw_data.get("itemId")).first()
        if listing:
            listing.db_status = -1
            listing.save()


def log_loop(event_filter):
    for event in event_filter.get_new_entries():
        handle_event(event)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            log_loop(block_filter)
            time.sleep(2)
