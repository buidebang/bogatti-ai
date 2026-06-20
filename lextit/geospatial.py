from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any

class LextitGeospatialOpportunityScorer:
    """
    Ingests granular geographic business data tables, calculates strategic priority metrics,
    and updates performance tracking records across the target network layers.
    """
    def calculate_opportunity_score(self, row_data: Dict[str, Any], local_city_average: float) -> Dict[str, Any]:
        # Using exact string parsing structures to eliminate floating-point calculation drift
        rating = Decimal(str(row_data.get("Rating", "0.0")))
        reviews = Decimal(str(row_data.get("Reviews_Count", "0")))
        city_avg = Decimal(str(local_city_average))
        fake_suspect = row_data.get("Fake_Suspect", "NO")

        score = Decimal("0.0")
        sales_pitch_strategy = "Basic Outreach Pattern / Standard Priority"

        if city_avg > Decimal("0.0") and rating > Decimal("0.0"):
            deviation = city_avg - rating
            # Increase opportunity score weight if rating falls below local averages
            weight_factor = deviation * Decimal("2.0") if deviation > Decimal("0.0") else Decimal("0.5")
            base_score = reviews * weight_factor

            if fake_suspect == "YES":
                base_score += Decimal("100.0") # Apply priority penalty weight for suspicious records

            score = base_score.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        # Enforce international outreach strategy routing criteria
        if score > Decimal("150") and row_data.get("Has_Verified_Email") == "YES":
            sales_pitch_strategy = "[URGENT_OUTREACH] High demand sector, profile metrics track below local baseline markets."
        elif fake_suspect == "YES" and row_data.get("Has_Verified_Email") == "YES":
            sales_pitch_strategy = "[ALERT_OUTREACH] Anomalous review profiles identified. Offer secure validation tooling."

        return {
            "entity_name": row_data.get("Name"),
            "calculated_opportunity_score": int(score),
            "targeted_sales_strategy": sales_pitch_strategy
        }
