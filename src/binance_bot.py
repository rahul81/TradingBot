import websocket, json
import numpy as np
import talib

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.05

in_position = False


closes = []


def on_open(ws):
    print("Connection opened")


def on_close(ws):
    print("Connection closed")


def on_message(ws, message):
    global closes
    print("Message received")
    json_message = json.loads(message)

    candle = json_message["k"]

    is_closed = candle["x"]
    close = candle["c"]

    if is_closed:
        print(f"Candle closed at {close}")
        closes.append(float(close))
        # print(f"Closes: {closes}")

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, timeperiod=RSI_PERIOD)
            print("All so far calculated: ")
            print(rsi)

            last_rsi = rsi[-1]

            print(f"Current RSI is : {last_rsi}")

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("OverBought !!, Sell!")
                    in_position = False
                else:
                    print("OverBought !!, not holding any ...")

            elif last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Oversold !!, already holding..")
                else:
                    print("Oversold !!, Buy!")
                    in_position = True


ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message
)
ws.run_forever()
