from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pandas as pd
import YahooAPI as yapi

def Order(obj):
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": "SEQUENT-EQ",
            "symboltoken": "14296",
            "transactiontype": "BUY",
            "exchange": "NSE",
            "ordertype": "MARKET",
            "producttype": "DELIVERY",
            "duration": "DAY",
            "price": "256",
            "quantity": "100",
            "triggerprice": "0"
            }
        orderId=obj.placeOrder(orderparams)
        #using the obj we initiated earlier
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e))

def place_order(obj, orderparams):
    try:
        orderID = obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderID))
    except Exception as e:
        print("Order placement failed: {}".format(e))

def place_multiple_orders(tradeList):
    with ThreadPoolExecutor() as executor:
        executor.map(place_order, tradeList)
