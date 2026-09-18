# ============================================
# SUPPLY CHAIN EFFICIENCY SCORE
# ============================================
import os
from .model_inference import predict_profit, predict_risk_probability, predict_shipping_days

def calculate_efficiency_score(
    profit,
    shipping_days,
    risk_probability
):

    score = 100

    # Penalize long shipping
    score -= shipping_days * 4

    # Penalize high risk
    score -= risk_probability * 0.3

    # Reward profit
    score += profit * 0.02

    # Clamp between 0 and 100
    score = max(0, min(100, score))

    return round(score, 2)


def calculate_efficiency_score_from_features(features):
    """Calculate efficiency score from a features mapping or iterable.

    This function uses the trained pipeline models to predict
    `shipping_days`, `risk_probability`, and `profit` from the provided
    raw features. If a model prediction is unavailable, it falls back to
    explicit numeric values in `features` when present.

    This is the Option B path: model-based prediction with the same
    scoring formula used for interpretability.
    """
    # try model predictions first
    pred_days = predict_shipping_days(features)
    pred_risk = predict_risk_probability(features)
    pred_profit = predict_profit(features)

    if isinstance(features, dict):
        profit_val = features.get("profit")
        days_val = features.get("shipping_days")
        risk_val = features.get("risk_probability")
    else:
        profit_val = days_val = risk_val = None

    if pred_profit is None and profit_val is None:
        return None
    if pred_days is None and days_val is None:
        return None
    if pred_risk is None and risk_val is None:
        return None

    profit_final = pred_profit if pred_profit is not None else profit_val
    days_final = pred_days if pred_days is not None else days_val
    risk_final = pred_risk if pred_risk is not None else risk_val

    return calculate_efficiency_score(profit_final, days_final, risk_final)


# ============================================
# EFFICIENCY LABEL
# ============================================

def efficiency_label(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 50:
        return "Moderate"

    else:
        return "Critical"


# ============================================
# BUSINESS RISK LEVEL
# ============================================

def business_risk_level(probability):

    if probability >= 80:
        return "Critical Risk"

    elif probability >= 60:
        return "High Risk"

    elif probability >= 40:
        return "Moderate Risk"

    else:
        return "Low Risk"


# ============================================
# AI RECOMMENDATIONS
# ============================================

def generate_recommendations(
    profit,
    shipping_days,
    risk_probability,
    shipping_mode
):

    recommendations = []

    if risk_probability >= 70:

        recommendations.append(
            "High delivery risk detected. Consider express shipping or regional warehouse allocation."
        )

    if shipping_days > 7:

        recommendations.append(
            "Shipping duration is high. Optimize route planning or use faster logistics partners."
        )

    if profit < 100:

        recommendations.append(
            "Low profit margin detected. Consider reducing discounts or increasing order quantity."
        )

    if shipping_mode == "Standard Class":

        recommendations.append(
            "Standard shipping selected. Upgrading shipping mode may reduce delay probability."
        )

    if not recommendations:

        recommendations.append(
            "Supply chain performance is operating efficiently."
        )

    return recommendations


# ============================================
# EXPLAINABLE AI
# ============================================

def generate_ai_explanation(
    shipping_days,
    risk_probability,
    profit
):

    explanations = []

    if shipping_days > 7:

        explanations.append(
            "Long shipping duration increases delay probability."
        )

    if risk_probability > 60:

        explanations.append(
            "High predicted delay risk impacts operational efficiency."
        )

    if profit < 100:

        explanations.append(
            "Low profit margins reduce business sustainability."
        )

    if not explanations:

        explanations.append(
            "Predictions indicate stable logistics performance."
        )

    return explanations