import os

from flask import Flask, render_template, request, send_file, send_from_directory
from utils.predictor import predict_all, build_input_dataframe
from utils.scenario_engine import generate_scenario_analysis
from utils.analytics import (
    calculate_efficiency_score,
    calculate_efficiency_score_from_features,
    efficiency_label,
    business_risk_level,
    generate_recommendations,
    generate_ai_explanation
)

app = Flask(__name__)

# ======================================================
# HOME PAGE
# ======================================================

@app.route('/')
def home():

    return render_template('index.html')


# ======================================================
# DASHBOARD
# ======================================================

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    result = None

    if request.method == 'POST':

        try:

            # ============================================
            # VALIDATION
            # ============================================

            distance = float(
                request.form['distance']
            )

            orders = int(
                request.form['orders']
            )

            product_price = float(
                request.form['product_price']
            )

            if (
                distance < 0 or
                orders < 0 or
                product_price < 0
            ):

                raise ValueError(
                    "Inputs cannot be negative."
                )

            # ============================================
            # GET ML PREDICTIONS
            # ============================================

            result = predict_all(
                request.form
            )

            model_input = build_input_dataframe(request.form)
            efficiency_score = calculate_efficiency_score_from_features(
                model_input
            )
            if efficiency_score is None:
                efficiency_score = calculate_efficiency_score(
                    result['predicted_profit'],
                    result['shipping_days'],
                    result['risk_probability']
                )

            efficiency_status = (
                efficiency_label(
                    efficiency_score
                )
            )

            business_risk = (
                business_risk_level(
                    result['risk_probability']
                )
            )

            recommendations = (
                generate_recommendations(

                    result['predicted_profit'],

                    result['shipping_days'],

                    result['risk_probability'],

                    request.form['shipping_mode']
                )
            )

            ai_explanations = (
                generate_ai_explanation(

                    result['shipping_days'],

                    result['risk_probability'],

                    result['predicted_profit']
                )
            )

            # ============================================
            # STORE ANALYTICS
            # ============================================

            result['efficiency_score'] = (
                efficiency_score
            )

            result['efficiency_status'] = (
                efficiency_status
            )

            result['business_risk'] = (
                business_risk
            )

            result['recommendations'] = (
                recommendations
            )

            result['ai_explanations'] = (
                ai_explanations
            )

        except Exception as e:

            result = {
                'error': str(e)
            }

    return render_template('dashboard.html', result=result )


@app.route('/powerbi-preview')
def powerbi_preview():

    return render_template('powerbi_preview.html')


# ===============================
# COMPARATIVE SCENARIO ANALYSIS
# ===============================


@app.route('/compare-scenarios', methods=['GET', 'POST'])
@app.route('/compare_scenarios', methods=['GET', 'POST'])
def compare_scenarios():

    if request.method == 'POST':

        try:

            scenarios = []

            for index in range(1, 4):

                distance_text = request.form.get(
                    f'distance_{index}',
                    '5'
                ).strip()
                orders_text = request.form.get(
                    f'orders_{index}',
                    '10'
                ).strip()
                product_price_text = request.form.get(
                    f'product_price_{index}',
                    '100'
                ).strip()
                shipping_mode = request.form.get(
                    f'shipping_mode_{index}',
                    'Road'
                )
                customer_segment = request.form.get(
                    f'customer_segment_{index}',
                    'Consumer'
                )
                market = request.form.get(
                    f'market_{index}',
                    'Africa'
                )
                order_city = request.form.get(
                    f'order_city_{index}',
                    'Unknown'
                ).strip()
                category_name = request.form.get(
                    f'category_name_{index}',
                    'Technology'
                )

                try:
                    distance = float(distance_text if distance_text else 5)
                    orders = int(orders_text if orders_text else 10)
                    product_price = float(product_price_text if product_price_text else 100)
                except ValueError:
                    raise ValueError(
                        f'Numeric values for scenario {index} must be valid numbers.'
                    )

                if distance < 0:
                    raise ValueError(
                        f'Shipping Days for scenario {index} cannot be negative.'
                    )

                if orders < 0:
                    raise ValueError(
                        f'Order Quantity for scenario {index} cannot be negative.'
                    )

                if product_price < 0:
                    raise ValueError(
                        f'Product Price for scenario {index} cannot be negative.'
                    )

                scenario_input = {
                    'distance': distance,
                    'orders': orders,
                    'product_price': product_price,
                    'shipping_mode': shipping_mode,
                    'customer_segment': customer_segment,
                    'market': market,
                    'order_city': order_city or 'Unknown',
                    'category_name': category_name
                }

                result = generate_scenario_analysis(scenario_input)

                scenario = {
                    'name': f'Scenario {index}',
                    'distance': distance,
                    'orders': orders,
                    'product_price': product_price,
                    'shipping_mode': shipping_mode,
                    'customer_segment': customer_segment,
                    'market': market,
                    'order_city': order_city or 'Unknown',
                    'category_name': category_name,
                    'predicted_shipping_days': result['predicted_shipping_days'],
                    'predicted_sales': result['predicted_sales'],
                    'predicted_profit': result['predicted_profit'],
                    'delay_risk': result['delay_risk'],
                    'transport_cost': result['transport_cost'],
                    'fuel_consumption': result['fuel_consumption'],
                    'carbon_emission': result['carbon_emission'],
                    'efficiency_score': result['efficiency_score'],
                    'sustainability_score': result['sustainability_score'],
                    'risk_probability': result['risk_probability']
                }

                scenarios.append(scenario)

            best_scenario = max(scenarios, key=lambda x: x['efficiency_score'])

            return render_template('compare_results.html', scenarios=scenarios, best_scenario=best_scenario)

        except Exception as e:
            return render_template('compare_form.html', error=str(e))

    else:

        return render_template('compare_form.html', error=None)


# ======================================================
# ANALYTICS PAGE
# ======================================================

@app.route('/analytics')
def analytics():
    return render_template('dashboard.html', result=None)


# ======================================================
# ROUTES PAGE
# ======================================================

@app.route('/routes')
def routes():
    return render_template('compare_results.html', scenarios=[], best_scenario=None)


# ======================================================
# AI REPORTS PAGE
# ======================================================

@app.route('/ai-reports')
def ai_reports():
    return render_template('results.html')


# ======================================================
# DEMO PAGE
# ======================================================

@app.route('/demo')
def demo():
    return render_template('dashboard.html', result=None)


# ======================================================
# RUN APP
# ======================================================

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'logo.jpg'
    )


if __name__ == '__main__':

    app.run(debug=True)