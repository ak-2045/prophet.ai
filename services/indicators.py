from typing import Dict

class IndicatorAnalyzer:
    
    def analyze(
        self,
        current_price: float,
        rsi: float,
        volume: str,
        sma_20: float | None = None,
        sma_50: float | None = None,
    ) -> Dict:

        analysis = {
            "rsi_signal": "",
            "volume_signal": "",
            "trend_signal": "",
            "overall_bias": "Neutral",
            "summary": []
        }

        bullish_score = 0
        bearish_score = 0

        # ---------------------------------
        # RSI Analysis
        # ---------------------------------
        if rsi >= 70:
            analysis["rsi_signal"] = (
                f"RSI is {rsi}, indicating overbought conditions. "
                "Momentum is strong but a pullback becomes increasingly possible."
            )
            bullish_score += 1

        elif rsi <= 30:
            analysis["rsi_signal"] = (
                f"RSI is {rsi}, indicating oversold conditions. "
                "Selling pressure may be exhausted and a bounce can occur."
            )
            bearish_score += 1

        else:
            analysis["rsi_signal"] = (
                f"RSI is {rsi}, suggesting healthy momentum "
                "without extreme conditions."
            )

        analysis["summary"].append(
            analysis["rsi_signal"]
        )

        # ---------------------------------
        # Volume Analysis
        # ---------------------------------
        if volume == "Increasing":
            analysis["volume_signal"] = (
                "Volume is increasing, confirming market participation "
                "and strengthening the current move."
            )

            bullish_score += 1

        elif volume == "Decreasing":
            analysis["volume_signal"] = (
                "Volume is decreasing, suggesting weakening conviction "
                "behind the current move."
            )

            bearish_score += 1

        else:
            analysis["volume_signal"] = (
                "Volume is neutral and does not provide strong confirmation."
            )

        analysis["summary"].append(
            analysis["volume_signal"]
        )

        # ---------------------------------
        # Moving Average Analysis
        # ---------------------------------
        if sma_20 is not None and sma_50 is not None:

            if current_price > sma_20 > sma_50:

                analysis["trend_signal"] = (
                    "Price is above both moving averages. "
                    "Short-term momentum aligns with the broader uptrend."
                )

                bullish_score += 2

            elif current_price < sma_20 < sma_50:

                analysis["trend_signal"] = (
                    "Price is below both moving averages. "
                    "Short-term weakness aligns with the broader downtrend."
                )

                bearish_score += 2

            else:
                analysis["trend_signal"] = (
                    "Moving averages are mixed and do not indicate "
                    "a clear directional bias."
                )

            analysis["summary"].append(
                analysis["trend_signal"]
            )

        # ---------------------------------
        # Overall Bias
        # ---------------------------------
        if bullish_score > bearish_score:
            analysis["overall_bias"] = "Bullish"

        elif bearish_score > bullish_score:
            analysis["overall_bias"] = "Bearish"

        else:
            analysis["overall_bias"] = "Neutral"

        return analysis