from typing import List, Dict, Optional


class MarketStructureAnalyzer:

    def analyze(
        self,
        prices: List[float],
        current_price: float,
        support: Optional[float],
        resistance: Optional[float],
        volume: str,
    ) -> Dict:

        result = {
            "structure": "Undetermined",
            "reason": "",
            "bias": "Neutral",
        }

        # Need enough data
        if len(prices) < 3:
            result["reason"] = (
                "At least three historical prices are required "
                "to determine market structure."
            )
            return result

        highs = []
        lows = []

        # Find local highs and lows
        for i in range(1, len(prices) - 1):

            if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
                highs.append(prices[i])

            if prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
                lows.append(prices[i])

        # ----------------------------
        # Bullish / Bearish Trend
        # ----------------------------
        if len(highs) >= 2 and len(lows) >= 2:

            last_high = highs[-1]
            previous_high = highs[-2]

            last_low = lows[-1]
            previous_low = lows[-2]

            if (
                last_high > previous_high
                and last_low > previous_low
            ):
                result["structure"] = "Bullish Trend"
                result["bias"] = "Bullish"
                result["reason"] = (
                    "Price is forming higher highs and higher lows, "
                    "indicating sustained buying pressure."
                )
                return result

            if (
                last_high < previous_high
                and last_low < previous_low
            ):
                result["structure"] = "Bearish Trend"
                result["bias"] = "Bearish"
                result["reason"] = (
                    "Price is forming lower highs and lower lows, "
                    "indicating sustained selling pressure."
                )
                return result

        # ----------------------------
        # If support/resistance unavailable
        # ----------------------------
        if support is None or resistance is None:
            result["reason"] = (
                "Support and resistance levels could not be determined "
                "from the available price data."
            )
            return result

        # ----------------------------
        # Bullish Breakout
        # ----------------------------
        if (
            current_price > resistance
            and volume == "Increasing"
        ):
            result["structure"] = "Bullish Breakout"
            result["bias"] = "Bullish"
            result["reason"] = (
                "Price has moved above resistance while volume is increasing. "
                "Participation from buyers is supporting the move."
            )
            return result

        # ----------------------------
        # Bearish Breakdown
        # ----------------------------
        if (
            current_price < support
            and volume == "Increasing"
        ):
            result["structure"] = "Bearish Breakdown"
            result["bias"] = "Bearish"
            result["reason"] = (
                "Price has moved below support while volume is increasing. "
                "Selling pressure is dominating the market."
            )
            return result

        # ----------------------------
        # Consolidation
        # ----------------------------
        price_range = resistance - support

        if price_range <= current_price * 0.02:
            result["structure"] = "Consolidation"
            result["bias"] = "Neutral"
            result["reason"] = (
                "Price is moving inside a very tight range, "
                "suggesting accumulation or indecision."
            )
            return result

        # ----------------------------
        # Range Bound
        # ----------------------------
        if support <= current_price <= resistance:
            result["structure"] = "Range Bound"
            result["bias"] = "Neutral"
            result["reason"] = (
                "Price is oscillating between support and resistance "
                "without establishing a clear trend."
            )
            return result

        return result