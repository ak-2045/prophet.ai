from typing import Dict

class RiskManager:
    """
    Handles trade risk calculations.

    Concepts:
    - Risk per Trade
    - Reward Potential
    - Risk : Reward Ratio
    - Position Sizing
    """

    def analyze(
        self,
        capital: float,
        risk_percent: float,
        entry: float,
        stop_loss: float,
        target: float
    ) -> Dict:

        result = {
            "capital": capital,
            "risk_percent": risk_percent,
            "risk_amount": 0.0,
            "risk_per_unit": 0.0,
            "reward_per_unit": 0.0,
            "risk_reward_ratio": 0.0,
            "position_size": 0,
            "summary": ""
        }

        # Amount willing to lose
        risk_amount = capital * (risk_percent / 100)

        # Risk per share/coin
        risk_per_unit = abs(entry - stop_loss)

        # Expected reward per share/coin
        reward_per_unit = abs(target - entry)

        if risk_per_unit == 0:
            result["summary"] = (
                "Entry and stop loss cannot be the same."
            )
            return result

        # Risk : Reward Ratio
        rr_ratio = reward_per_unit / risk_per_unit

        # Maximum units to buy
        position_size = int(
            risk_amount / risk_per_unit
        )

        result["risk_amount"] = round(
            risk_amount, 2
        )

        result["risk_per_unit"] = round(
            risk_per_unit, 2
        )

        result["reward_per_unit"] = round(
            reward_per_unit, 2
        )

        result["risk_reward_ratio"] = round(
            rr_ratio, 2
        )

        result["position_size"] = position_size

        # Educational explanation
        if rr_ratio >= 3:
            quality = "Excellent"

        elif rr_ratio >= 2:
            quality = "Good"

        elif rr_ratio >= 1:
            quality = "Average"

        else:
            quality = "Poor"

        result["summary"] = (
            f"You are risking {result['risk_amount']} "
            f"to potentially earn "
            f"{round(position_size * reward_per_unit, 2)}. "
            f"The trade has a "
            f"1:{result['risk_reward_ratio']} "
            f"risk-reward ratio, which is considered "
            f"{quality.lower()}."
        )

        return result