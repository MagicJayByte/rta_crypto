from binance import ThreadedWebsocketManager
import csv
import pandas as pd

def handle_socket_message(msg):
    print(f"Symbol: {msg['s']} | Close: {msg['k']['c']} | Time: {msg['k']['t']}")

twm = ThreadedWebsocketManager()
twm.start()

symbols = ["btcusdt", "ethusdt", "solusdt"]  # Lowercase for WebSocket
intervals = ["1s", "5s"]  # Supported in WebSocket

for symbol in symbols:
    for interval in intervals:
        twm.start_kline_socket(
            callback=handle_socket_message,
            symbol=symbol,
            interval=interval
        )


def handle_socket_message(msg):
    data = {
        "symbol": msg['s'],
        "timestamp": pd.to_datetime(msg['k']['t'], unit='ms'),
        "close": float(msg['k']['c'])
    }
    with open("crypto_prices.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if f.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(data)