from flask import Flask, request, json, jsonify
import requests
from orderbook_ticker import OrderBookTicker
from adlisting_ticker import AdListingTicker

app = Flask(__name__)
app.config.from_object('env')

@app.route("/orderbook")
def orderbook():
  bitven_url = 'https://bitven.com/assets/js/rates.js'
  bitven_json = requests.get(bitven_url).json()

  BTC_TO_USD_RATE = bitven_json['BTC_TO_USD_RATE']
  orderbook_url = 'https://localbitcoins.com/bitcoincharts/ves/orderbook.json'
  orderbook_json = requests.get(orderbook_url).json()

  ticker = OrderBookTicker(orderbook_json, BTC_TO_USD_RATE)
  result = ticker.compute()

  return jsonify(result)

@app.route("/listing")
def listing():
  bitven_url = 'https://bitven.com/assets/js/rates.js'
  bitven_json = requests.get(bitven_url).json()

  BTC_TO_USD_RATE = bitven_json['BTC_TO_USD_RATE']
  MIN_BTC_THRESHOLD = 0.001
  USD_TO_VES_RATE = bitven_json['USD_TO_BSF_RATE']
  MIN_USD_THRESHOLD = round(MIN_BTC_THRESHOLD*BTC_TO_USD_RATE, 2)
  MIN_VES_THRESHOLD = round(MIN_USD_THRESHOLD*USD_TO_VES_RATE, 2)

  sell_url = 'https://localbitcoins.com/sell-bitcoins-online/VES/.json?fields=min_amount,max_amount,profile,ad_id,bank_name,temp_price'
  sells_json = requests.get(sell_url).json()

  buy_url = 'https://localbitcoins.com/buy-bitcoins-online/VES/.json?fields=min_amount,max_amount,profile,ad_id,bank_name,temp_price'
  buys_json = requests.get(buy_url).json()

  orderbook_json = {
      'bids': buys_json,
      'asks': sells_json,
  }

  ticker = AdListingTicker(orderbook_json, BTC_TO_USD_RATE)
  result = ticker.compute()

  return jsonify(result)
