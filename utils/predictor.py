import joblib
import pandas as pd

# ============================================
# LOAD MODELS ONLY ONCE
# ============================================

shipping_days_model = joblib.load(
    'models/Days_of_shipping_linear.pkl'
)

late_delivery_model = joblib.load(
    'models/Latedelivery_logistic.pkl'
)

sales_model = joblib.load(
    'models/Saleslinear.pkl'
)

profit_model = joblib.load(
    'models/OPPOlinear.pkl'
)

customer_segment_model = joblib.load(
    'models/CustSegmentlogistic.pkl'
)

delivery_status_model = joblib.load(
    'models/DelStatuslogistic.pkl'
)

# ============================================
# INPUT BUILDER
# ============================================

def build_input_dataframe(data):

    distance = float(data['distance'])
    orders = int(data['orders'])
    product_price = float(data['product_price'])

    shipping_mode = data['shipping_mode']
    customer_segment = data['customer_segment']
    market = data['market']
    order_city = data['order_city']
    category_name = data['category_name']

    return pd.DataFrame([{

        'Product Price': product_price,

        'Order Item Quantity': orders,

        'Shipping Mode': shipping_mode,

        'Customer Segment': customer_segment,

        'Market': market,

        'Category Name': category_name,

        'Order City': order_city,

        'Days for shipment (scheduled)': distance,

        'Order Item Product Price': product_price,

        'Order Item Discount Rate': 0.10,

        'Order Item Discount': (
            product_price * orders * 0.10
        ),

        'Order Item Total': (
            product_price * orders
        ),

        'Product Category Id': 1,

        'Sales': (
            product_price * orders
        ),

        'Order Item Profit Ratio': 0.25,

        'Late_delivery_risk': 0,

        'Order Region': 'Africa',

        'Order Status': 'COMPLETE'

    }])


# ============================================
# MAIN PREDICTION FUNCTION
# ============================================

def predict_all(data):

    input_df = build_input_dataframe(data)

    # ============================================
    # PREDICTIONS
    # ============================================

    predicted_sales = float(
        sales_model.predict(input_df)[0]
    )

    predicted_profit = float(
        profit_model.predict(input_df)[0]
    )

    predicted_shipping_days = float(
        shipping_days_model.predict(input_df)[0]
    )

    late_delivery_prediction = (
        late_delivery_model.predict(input_df)[0]
    )

    delivery_status_prediction = (
        delivery_status_model.predict(input_df)[0]
    )

    customer_segment_prediction = (
        customer_segment_model.predict(input_df)[0]
    )

    # ============================================
    # PROBABILITY
    # ============================================

    try:

        probability = late_delivery_model.predict_proba(
            input_df
        )[0][1]

        probability = round(
            probability * 100,
            2
        )

    except:

        probability = 0

    # ============================================
    # RISK STATUS
    # ============================================

    if late_delivery_prediction == 1:

        risk_status = "High Risk"

        late_delivery_status = (
            "Likely Late Delivery"
        )

    else:

        risk_status = "Low Risk"

        late_delivery_status = (
            "On-Time Delivery"
        )

    # ============================================
    # RETURN RESULTS
    # ============================================

    return {

        'predicted_sales': round(
            predicted_sales,
            2
        ),

        'predicted_profit': round(
            predicted_profit,
            2
        ),

        'shipping_days': round(
            predicted_shipping_days,
            2
        ),

        'late_delivery': late_delivery_status,

        'delivery_status': str(
            delivery_status_prediction
        ).title(),

        'customer_segment': str(
            customer_segment_prediction
        ).title(),

        'risk_status': risk_status,

        'risk_probability': probability
    }