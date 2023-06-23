from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import websocket
import smtplib

import json

# init
api_key = ''#Enter your api key here
api_secret = ''#Enter your secret key here
client = Client(api_key, api_secret)
socket = "wss://stream.binance.com:9443/ws/maticusdt@miniTicker"
#This bot is for matic to change it any other crypto just replace matic with crypto of your choice in above link
bought = 0
x = 999999999999
y = 0.01
quantity = 0


def email_buy(bought, crypto):
    global quantity
    bought = float(round(bought, 4))
    quantity = 12 / bought 
    quantity = float(round(quantity, 2))
    # BUY
    try:
        buy_limit = client.create_order(
            symbol='MATICUSDT',
            #This bot is for matic to change it any other crypto just replace matic with crypto of your choice in above code
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

    subject = "bought at" + " " + str(bought) + " " + crypto + "  succesful"
    email_user = ''#Enter the email id throught which you want to send email alerts
    email_password = ''#Enter the email id password throught which you want to send email alerts
    email_send = ''#Enter the email id on which you want to get alerts
    text = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    print("Done")


def email_sell(sold, crypto):
    global quantity
    quantity = float(round(quantity, 2))
    sold = float(round(sold, 4))
    try:
        sell_limit = client.create_order(
            symbol='MATICUSDT',
            #This bot is for matic to change it any other crypto just replace matic with crypto of your choice in above code
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

    subject = "sold at" + " " + str(sold) + " " + crypto + "  succesful"
    email_user = ''#Enter the email id throught which you want to send email alerts
    email_password = ''#Enter the email id password throught which you want to send email alerts
    email_send = ''#Enter the email id on which you want to get alerts
    text = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    print("Done")


def on_message(ws, message):
    json_message = json.loads(message)
    buy = float(json_message['c'])
    high = float(json_message['h'])
    low = float(json_message['l'])
    sell = buy
    avg = (high + low) / 2
    global bought
    global x
    global y
    if bought == 0:
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
        mini_profit = bought + (bought * 4) / 100
        max_loss = bought - (bought * 15) / 100
        if sell >= mini_profit:
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
        elif sell <= max_loss:
            sold = max_loss
            print("sold at loss")
            email_sell(sold, "matic")


def on_close(ws):
    print("connection close")
    subject = "connection closed matic"
    email_user = ''#Enter the email id throught which you want to send email alerts
    email_password = ''#Enter the email id password throught which you want to send email alerts
    email_send = ''#Enter the email id on which you want to get alerts
    text = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()
    print("Done")


ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)

ws.run_forever()
