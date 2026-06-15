from typing import Dict

class TradeSetupGenerator:
    """
    Generates educational trade setups based on
    market structure and indicator analysis.

    This is NOT a signal generator.
    It only creates explainable trade scenarios.
    """

    def generate(
        self,
        current_price: float,
        support: float,
        resistance: float,
        market_structure: Dict,
        indicators: Dict,
        risk: Dict
    ) -> Dict:

        structure = market_structure["structure"]
        bias = indicators["overall_bias"]

        setup = {
            "trade_type": "No Trade",
            "entry": None,
            "stop_loss": None,
            "target": None,
            "confidence": "Low",
            "reasons": [],
            "warnings": []
        }

        # ----------------------------------
        # Bullish Setups
        # ----------------------------------
        if (
            structure in ["Bullish Trend", "Bullish Breakout"]
            and bias == "Bullish"
        ):

            entry = resistance
            stop_loss = support

            risk_per_unit = abs(
                entry - stop_loss
            )

            target = entry + (
                risk_per_unit * 2
            )

            setup["trade_type"] = "Long"
            setup["entry"] = round(entry, 2)
            setup["stop_loss"] = round(stop_loss, 2)
            setup["target"] = round(target, 2)
            setup["confidence"] = "High"

            setup["reasons"] = [
                market_structure["reason"],
                indicators["rsi_signal"],
                indicators["volume_signal"]
            ]

            if risk["risk_reward_ratio"] < 2:
                setup["warnings"].append(
                    "Risk-reward ratio is below 1:2."
                )

            return setup

        # ----------------------------------
        # Bearish Setups
        # ----------------------------------
        if (
            structure in ["Bearish Trend", "Bearish Breakdown"]
            and bias == "Bearish"
        ):

            entry = support
            stop_loss = resistance

            risk_per_unit = abs(
                stop_loss - entry
            )

            target = entry - (
                risk_per_unit * 2
            )

            setup["trade_type"] = "Short"
            setup["entry"] = round(entry, 2)
            setup["stop_loss"] = round(stop_loss, 2)
            setup["target"] = round(target, 2)
            setup["confidence"] = "High"

            setup["reasons"] = [
                market_structure["reason"],
                indicators["rsi_signal"],
                indicators["volume_signal"]
            ]

            if risk["risk_reward_ratio"] < 2:
                setup["warnings"].append(
                    "Risk-reward ratio is below 1:2."
                )

            return setup

        # ----------------------------------
        # Neutral Markets
        # ----------------------------------
        if structure in [
            "Range Bound",
            "Consolidation"
        ]:

            setup["trade_type"] = "Wait"

            setup["warnings"] = [
                "Market lacks clear direction.",
                "Breakout confirmation is required before considering a trade.",
                "Avoid forcing trades during consolidation."
            ]

            return setup

        # ----------------------------------
        # Default
        # ----------------------------------
        setup["warnings"] = [
            "No high-probability setup detected."
        ]

        return setup