from datetime import timedelta

import yfinance as yf
from django.utils import timezone

from .models import StockPrice


def fetch_and_store_if_needed(symbol):
    should_fetch = False

    try:
        latest_stock = StockPrice.objects.filter(symbol=symbol).latest("last_updated")
        if timezone.now() - latest_stock.last_updated > timedelta(minutes=15):
            print(f"Data for {symbol} is stale. Fetching new data.")
            should_fetch = True
        else:
            print(f"Data for {symbol} is fresh. Using cached data from DB.")

    except StockPrice.DoesNotExist:
        print(f"No data for {symbol} found. Fetching initial data.")
        should_fetch = True

    if should_fetch:
        try:
            print(f"--- Attempting to fetch data for {symbol} from yfinance ---")
            stock = yf.Ticker(symbol)
            data = stock.history(period="6mo", interval="1d")

            if data.empty:
                print(f"yfinance returned no data for {symbol}.")
                return

            StockPrice.objects.filter(symbol=symbol).delete()

            prices_to_create = []
            for index, row in data.iterrows():
                prices_to_create.append(
                    StockPrice(
                        symbol=symbol,
                        date=index.date(),
                        open=row["Open"],
                        high=row["High"],
                        low=row["Low"],
                        close=row["Close"],
                        volume=row["Volume"],
                        last_updated=timezone.now(),
                    )
                )

            StockPrice.objects.bulk_create(prices_to_create)
            print(f"--- Successfully fetched and stored new data for {symbol} ---")

        except yf.exceptions.YFRateLimitError:
            print(
                f"!!! YFINANCE RATE LIMIT ERROR for {symbol}. "
                "Skipping fetch. The app will use old data. !!!"
            )
            pass
        except Exception as e:
            print(
                f"!!! An unexpected error occurred while fetching data for {symbol}: {e} !!!"
            )
            pass
