from web3 import Web3
from django.apps import AppConfig
import time
import json
import threading

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))
with open("contract_abi.json") as f:
    info_json = json.load(f)
abi = info_json
contractAddress = '0x4389BB94789D00bC106C176351b36dBd9dA69817'
contract = w3.eth.contract(address=contractAddress, abi=abi)
block_filter = w3.eth.filter({'fromBlock': 'latest', 'address': contractAddress})


def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = contract.events.greeting.processReceipt(receipt)
    print(result[0]['args'])


def log_loop(event_filter, poll_interval):
    for event in event_filter.get_new_entries():
        handle_event(event)
        time.sleep(poll_interval)


class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            log_loop(block_filter, 2000)


class MarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.market'

    def ready(self):
        from apps.market import signals
        t = BackgroundTasks()
        t.start()
