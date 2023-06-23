import config
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(config.api_key, config.api_secret)
socket = "wss://stream.binance.com:9443/ws/maticusdt@miniTicker"


buy_orders = []
sell_orders = []

