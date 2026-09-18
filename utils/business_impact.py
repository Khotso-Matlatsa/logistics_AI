def calculate_delivery_cost(distance, fuel_cost):

    fuel_efficiency = 12  # km per litre

    litres_used = distance / fuel_efficiency

    total_cost = litres_used * fuel_cost

    return round(total_cost, 2)