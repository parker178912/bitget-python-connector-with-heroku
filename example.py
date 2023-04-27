import bitget_python_connector.mix.market_api as market
import bitget_python_connector.mix.account_api as accounts
import bitget_python_connector.mix.position_api as position
import bitget_python_connector.mix.order_api as order
import bitget_python_connector.mix.plan_api as plan
import bitget_python_connector.mix.trace_api as trace
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

api_key = ""
secret_key = ""
passphrase = ""

market_config = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
order_config = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
account_config = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
trace_config = trace.TraceApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

def open(symbol, size, side, stoplossprice = None, takeprofit = None):
    try:
        print(f"sending order - {side} {size} {symbol}")
        result = order_config.place_order(symbol, marginCoin='USDT', size=size, side=side, orderType='market', timeInForceValue='normal', presetStopLossPrice=stoplossprice, presetTakeProfitPrice = takeprofit)
        print(result)
    except Exception as e:
        print("an exception occured - {}".format(e))
    return

def close(symbol, closeside):
    try:
        findorder = trace_config.current_track(symbol = symbol,productType='umcbl',pageSize=20,pageNo=1)
        datalen = len(findorder['data'])
        if datalen!=0:
            for i in range(datalen):
                if findorder['data'][i]['holdSide'] == closeside:
                    trackno = findorder['data'][i]['trackingNo']
                    print(trackno)
                    trace_config.close_track_order(symbol, trackno)
                    break
    except Exception as e:
        print("an exception occured - {}".format(e))
    return

@app.route('/normal', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    symbol = "ETHUSDT_UMCBL"
    size = 0.1
    market_position = data['strategy']['market_position']
    pre_market_position = data['strategy']['prev_market_position']
    action = data['strategy']['order_action']
    try:
        stoplossprice = str(int(data['strategy']['stopLossPrice']*100)/100)
        takeprofit = str(int(data['strategy']['takeprofit']*100)/100)
    except:
        stoplossprice = None
        takeprofit = None
    if(market_position == "flat" and action == "buy"): #close short
        open(symbol, size, "close_short")
    elif(market_position == "flat" and action == "sell"): #close long
        open(symbol, size, "close_long")
    elif(market_position == "long" and action == "buy" and pre_market_position == "flat"): #long entry
        open(symbol, size, "open_long", stoplossprice, takeprofit)
    elif(market_position == "short" and action == "sell" and pre_market_position == "flat"): #short entry
        open(symbol, size, "open_short", stoplossprice, takeprofit)
    elif(market_position == "long" and action == "buy" and pre_market_position == "short"): #close short and open long
        open(symbol, size, "close_short")
        open(symbol, size, "open_long", stoplossprice, takeprofit)
    elif(market_position == "short" and action == "sell" and pre_market_position == "long"): #close long and open short
        open(symbol, size, "close_long")
        open(symbol, size, "open_short", stoplossprice, takeprofit)     
    return{
        "message":"success",
    }

@app.route('/trader', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    symbol = "ETHUSDT_UMCBL"
    size = 0.1
    market_position = data['strategy']['market_position']
    pre_market_position = data['strategy']['prev_market_position']
    action = data['strategy']['order_action']
    try:
        stoplossprice = str(int(data['strategy']['stopLossPrice']*100)/100)
        takeprofit = str(int(data['strategy']['takeprofit']*100)/100)
    except:
        stoplossprice = None
        takeprofit = None
    if(market_position == "flat" and action == "buy"): #close short
        close(symbol, "short")
    elif(market_position == "flat" and action == "sell"): #close long
        close(symbol, "long")
    elif(market_position == "long" and action == "buy" and pre_market_position == "flat"): #long entry
        open(symbol, size, "open_long", stoplossprice, takeprofit)
    elif(market_position == "short" and action == "sell" and pre_market_position == "flat"): #short entry
        open(symbol, size, "open_short", stoplossprice, takeprofit)
    elif(market_position == "long" and action == "buy" and pre_market_position == "short"): #close short and open long
        close(symbol, "short")
        open(symbol, size, "open_long", stoplossprice, takeprofit)
    elif(market_position == "short" and action == "sell" and pre_market_position == "long"): #close long and open short
        close(symbol, "long")
        open(symbol, size, "open_short", stoplossprice, takeprofit)     
    return{
        "message":"success",
    }    