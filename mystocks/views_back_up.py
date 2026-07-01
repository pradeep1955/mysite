import base64
import io

import matplotlib
import pandas as pd
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .gpt_commentary import generate_gpt_comment
from .models import StockPrice
from .utils import fetch_and_store_if_needed

matplotlib.use("Agg")
import matplotlib.pyplot as plt


@xframe_options_exempt
def stock_chart(request):
    symbol = request.GET.get("symbol", "SBIN.BO")
    favorite_stocks = ["SBIN.BO", "TCS.BO", "INFY.BO"]

    fetch_and_store_if_needed(symbol)
    data = StockPrice.objects.filter(symbol=symbol).order_by("date")

    chart = None
    comment = "No data available for this stock."

    if data.exists():
        df = pd.DataFrame(list(data.values("date", "close", "volume")))
        df.set_index("date", inplace=True)

        df["SMA50"] = df["close"].rolling(window=50).mean()
        df["SMA200"] = df["close"].rolling(window=200).mean()

        df["EMA12"] = df["close"].ewm(span=12, adjust=False).mean()
        df["EMA26"] = df["close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = df["EMA12"] - df["EMA26"]
        df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()
        rs = avg_gain / avg_loss.replace(0, 0.000001)
        df["RSI"] = 100 - (100 / (1 + rs))

        latest_rsi = df["RSI"].iloc[-1]
        latest_macd = df["MACD"].iloc[-1]
        latest_signal = df["Signal"].iloc[-1]
        comment = generate_gpt_comment(symbol, latest_rsi, latest_macd, latest_signal)

        plt.style.use("dark_background")
        fig, axs = plt.subplots(4, 1, figsize=(12, 14), sharex=True)
        fig.patch.set_facecolor("#121212")
        for ax in axs:
            ax.set_facecolor("#212121")
            ax.grid(True, linestyle="--", alpha=0.5)

        axs[0].plot(df.index, df["close"], label="Close Price", color="#00c8ff")
        axs[0].plot(df.index, df["SMA50"], label="SMA 50", color="#ffb347")
        axs[0].plot(df.index, df["SMA200"], label="SMA 200", color="#ff4040")
        axs[0].set_title(f"Price & Moving Averages for {symbol}")
        axs[0].legend()

        axs[1].bar(df.index, df["volume"], label="Volume", color="grey")
        axs[1].set_title("Trading Volume")
        axs[1].legend()

        axs[2].plot(df.index, df["MACD"], label="MACD", color="g")
        axs[2].plot(df.index, df["Signal"], label="Signal Line", color="r")
        axs[2].set_title("MACD")
        axs[2].legend()

        axs[3].plot(df.index, df["RSI"], label="RSI", color="purple")
        axs[3].axhline(70, color="red", linestyle="--")
        axs[3].axhline(30, color="green", linestyle="--")
        axs[3].set_title("Relative Strength Index (RSI)")
        axs[3].legend()

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close(fig)

    context = {
        "chart": chart,
        "symbol": symbol,
        "favorite_stocks": favorite_stocks,
        "comment": comment,
    }
    return render(request, "mystocks/stock_chart.html", context)


@api_view(["POST"])
def stock_predict_api(request):
    symbol = request.data.get("symbol")
    rsi = request.data.get("rsi")
    macd = request.data.gfet("macd")
    signal = request.data.get("signal")

    if not all([symbol, rsi, macd, signal]):
        return Response({"error": "Missing required input data"}, status=400)

    try:
        comment = generate_gpt_comment(symbol, float(rsi), float(macd), float(signal))
        return Response({"comment": comment})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


def test_internet(request):
    try:
        response = requests.get("https://api.openai.com/v1", timeout=5)
        return HttpResponse(
            f"Successfully connected to OpenAI API. Status: {response.status_code}"
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Connection Error: {e}")
