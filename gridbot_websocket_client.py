from email import message
import websocket
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import websocket,json,config

ws_j = websocket.WebSocket()
ws_j.connect("ws://localhost:9001")

client = Client(config.api_key,config.api_secret)
socket = "wss://stream.binance.com:9443/ws/btcusdt@miniTicker"

x = 999999999999
y = 0.01
quantity=0
bought = 1.604
h = 0
orders = client.get_all_orders(symbol='MATICUSDT', limit=10)
for i in range(10):
    if orders[i]['side'] == 'SELL':
        message_ini = "sold at "
        message_ini = message_ini + str(orders[i]['price'])
        ws_j.send(json.dumps(message_ini))
    else:
        message_ini = "bought at "
        message_ini = message_ini + str(orders[i]['price'])
        ws_j.send(json.dumps(message_ini))
def email_buy(bought,crypto):
    global quantity
    bought = float(round(bought, 5))
    quantity = 11/bought
    quantity = float(round(quantity, 1))
    message = "bought at "
    message = message + str(bought)
    ws_j.send(json.dumps(message))
    # BUY
    try:
        buy_limit = client.create_test_order(
            symbol='MATIUSDT',
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=bought)
    except BinanceAPIException as e:
        # error handling goes here
        error = e
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        error = e
        print(e)
    print("Done")






def email_sell(sold,crypto):
    global quantity
    quantity = float(round(quantity, 1))
    sold = float(round(sold, 5))
    print("sell",sold)
    print(sold)
    message = "sold at "
    message = message + str(sold)
    ws_j.send(json.dumps(message))
    try:
        sell_limit = client.create_test_order(
            symbol='MATICUSDT',
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=sold)
    except BinanceAPIException as e:
        # error handling goes here
        error = e
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        error = e
        print(e)


    print("Done")



def on_message(ws,message):
    json_message = json.loads(message)
    buy = float(json_message['c'])
    high= float(json_message['h'])
    low= float(json_message['l'])
    sell = buy
    avg = (high + low)/2
    global h
    global bought
    global x
    global y
    print(buy)
    change = ((high - avg)*100)/avg
    if bought == 0 and change >=3:
        if buy < avg:
            temp = buy
            if temp < x:
                x = temp
            elif temp >= x + (x * 2) / 100:
                print("buy")
                bought = temp
                print(bought)
                email_buy(bought, "matic")

    else:
        mini_profit = bought + (bought * 3.5) / 100
        if sell >= mini_profit and bought!=0:
            temp = sell
            if temp > y:
                y = temp
            elif temp <= y - (y * 2) / 100:
                print("sold")
                sold = temp
                bought = 0
                print("sold")
                print(sold)
                email_sell(sold, "matic")

def on_close(ws):
    print("connection close")
    print("Done")

ws = websocket.WebSocketApp(socket,on_message=on_message,on_close=on_close)
ws.run_forever()

