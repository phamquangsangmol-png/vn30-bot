import requests
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator

TOKEN = "8685395607:AAETpbeO7dYiwyVOcodT-q5cg7HGAjOLhXs"
CHAT_ID = "5938672813"

stocks = [
    "FPT.VN","HPG.VN","SSI.VN","MWG.VN","VCB.VN",
    "TCB.VN","VNM.VN","MBB.VN","ACB.VN","VPB.VN"
]

results = []

for stock in stocks:

    data = yf.download(stock, period="3mo", interval="1d", progress=False)

    if data.empty or len(data) < 20:
        continue

    rsi = RSIIndicator(data['Close'].squeeze()).rsi()
    latest_rsi = rsi.iloc[-1]

    price = data['Close'].iloc[-1]

    if latest_rsi < 60:
        signal = "BUY 🟢"
        results.append(f"{stock} | Price: {round(price,2)} | RSI: {round(latest_rsi,1)}")

message = "📊 VN30 SIGNAL\n\n"

if results:
    message += "\n".join(results)
else:
    message += "Không có tín hiệu hôm nay"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})