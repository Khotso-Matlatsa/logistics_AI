from utils.predictor import build_input_dataframe, predict_all
from utils.analytics import calculate_efficiency_score_from_features


def generate_scenario_analysis(data):

    input_df = build_input_dataframe(data)
    result = predict_all(data)

    efficiency_score = calculate_efficiency_score_from_features(input_df)
    delay_risk = 75 if result['risk_probability'] >= 50 else 20

    transport_cost = round(
        result['shipping_days'] * 45 + int(data.get('orders', 10)) * 12 + float(data.get('product_price', 100.0)) * 0.08,
        2
    )

    fuel_consumption = round(
        result['shipping_days'] * 8 + int(data.get('orders', 10)) * 1.5,
        2
    )

    carbon_emission = round(fuel_consumption * 0.75, 2)

    sustainability_score = round(
        max(0, (efficiency_score or 0) / (carbon_emission + 1) * 100),
        2
    )

    return {
        'delay_risk': delay_risk,
        'transport_cost': transport_cost,
        'fuel_consumption': fuel_consumption,
        'carbon_emission': carbon_emission,
        'efficiency_score': efficiency_score,
        'sustainability_score': sustainability_score,
        'predicted_shipping_days': result['shipping_days'],
        'predicted_sales': result['predicted_sales'],
        'predicted_profit': result['predicted_profit'],
        'risk_probability': result['risk_probability']
    }