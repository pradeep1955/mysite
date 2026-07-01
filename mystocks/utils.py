import logging

import pandas as pd
import yfinance as yf
from django.utils import timezone

from .models import StockPrice

logger = logging.getLogger(__name__)


def fetch_and_store_if_needed(symbol):
    should_fetch = False
    latest_stock = None

    try:
        latest_stock = StockPrice.objects.filter(symbol=symbol).latest("last_updated")
        today_date = timezone.now().date()
        if latest_stock.last_updated.date() < today_date:
            logger.debug(
                "Data for %s is from a previous day (%s). Fetching new data for %s.",
                symbol,
                latest_stock.last_updated.date(),
                today_date,
            )
            should_fetch = True
        else:
            logger.debug(
                "Data for %s is up-to-date for today (%s). Using cached data from DB.",
                symbol,
                latest_stock.last_updated.date(),
            )
            return latest_stock

    except StockPrice.DoesNotExist:
        logger.debug("No data for %s found. Fetching initial data.", symbol)
        should_fetch = True

    if should_fetch:
        try:
            logger.debug("Attempting to fetch data for %s from yfinance", symbol)
            stock = yf.Ticker(symbol)
            data = stock.history(period="6mo", interval="1d")

            if data.empty:
                logger.warning(
                    "yfinance returned no data for %s. Returning old data if available.",
                    symbol,
                )
                return latest_stock

            StockPrice.objects.filter(symbol=symbol).delete()

            prices_to_create = []
            for index, row in data.iterrows():
                if any(pd.isna(row[col]) for col in ["Open", "High", "Low", "Close", "Volume"]):
                    logger.warning(
                        "Skipping row for %s on %s due to NaN values.",
                        symbol,
                        index.date(),
                    )
                    continue

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

            if prices_to_create:
                StockPrice.objects.bulk_create(prices_to_create)
                logger.debug("Successfully fetched and stored new data for %s", symbol)
                latest_stock = StockPrice.objects.filter(symbol=symbol).latest("date")
                return latest_stock

            logger.warning(
                "No valid price data found for %s after filtering NaNs. Returning old data.",
                symbol,
            )
            return latest_stock

        except Exception as e:
            logger.error(
                "An unexpected error occurred fetching %s: %s",
                symbol,
                e,
                exc_info=True,
            )
            return latest_stock

    return latest_stock
