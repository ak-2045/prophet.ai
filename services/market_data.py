import yfinance as yf
import pandas as pd


class MarketDataService:
    

    def __init__(self):
        self.ticker = None

    # ----------------------------------
    # Set Asset
    # ----------------------------------
    def set_asset(
        self,
        symbol: str
    ) -> None:

        self.ticker = yf.Ticker(symbol)

    # ----------------------------------
    # Current Market Information
    # ----------------------------------
    def get_market_info(self) -> dict:

        if self.ticker is None:
            raise ValueError(
                "Asset not selected."
            )

        info = self.ticker.info

        return {
            "name":
                info.get(
                    "longName",
                    "Unknown Asset"
                ),

            "symbol":
                info.get(
                    "symbol"
                ),

            "currency":
                info.get(
                    "currency"
                ),

            "exchange":
                info.get(
                    "exchange"
                ),

            "current_price":
                info.get(
                    "currentPrice"
                ),

            "previous_close":
                info.get(
                    "previousClose"
                ),

            "day_high":
                info.get(
                    "dayHigh"
                ),

            "day_low":
                info.get(
                    "dayLow"
                ),

            "volume":
                info.get(
                    "volume"
                ),

            "market_cap":
                info.get(
                    "marketCap"
                )
        }

    # ----------------------------------
    # Historical OHLC Data
    # ----------------------------------
    def get_history(
        self,
        period: str = "3mo",
        interval: str = "1d"
    ) -> pd.DataFrame:

        if self.ticker is None:
            raise ValueError(
                "Asset not selected."
            )

        df = self.ticker.history(
            period=period,
            interval=interval
        )

        if df.empty:
            raise ValueError(
                "No historical data found."
            )

        return df[
            [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        ]
