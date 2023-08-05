from flask import Flask, request, jsonify
import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
from datetime import datetime, timedelta
import Helper.JsonReader as jsonHelper
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.BollingerBand as bband
import Service.SignalGenerator as signalSer

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "AJITH",
        "email": "bajithcnb@gmail.com"
    }
    # "get-user/123?extra=hello world"
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    return jsonify(data), 201

@app.route("/getsignal-basedonindicator", methods=["POST"])
def getSignalBasedOnIndicator():
    data = request.get_json()

    result = signalSer.tradingSignal(data)
  
    return jsonify(result), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)