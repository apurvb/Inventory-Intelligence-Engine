HOLDING_COST_RATE = 0.25
STOCKOUT_COST_MULTIPLIER = 2.0

def calculate_holding_cost(excess_units: float, unit_cost: float, days: int = 365) -> float:
    annual_holding = excess_units * unit_cost * HOLDING_COST_RATE
    return round(annual_holding * (days / 365), 2)

def calculate_stockout_cost(shortage_units: float, unit_cost: float) -> float:
    return round(shortage_units * unit_cost * STOCKOUT_COST_MULTIPLIER, 2)

def calculate_transfer_savings(
    excess_units: float,
    shortage_units: float,
    unit_cost: float,
    transfer_cost_per_unit: float = 2.0
) -> dict:
    transferable = min(excess_units, shortage_units)
    stockout_cost_avoided = calculate_stockout_cost(transferable, unit_cost)
    transfer_cost = round(transferable * transfer_cost_per_unit, 2)
    net_savings = round(stockout_cost_avoided - transfer_cost, 2)

    return {
        "transferable_units": round(transferable, 2),
        "stockout_cost_avoided": stockout_cost_avoided,
        "transfer_cost": transfer_cost,
        "net_savings": net_savings,
    }

def simulate_financial_impact(imbalance_results: list[dict]) -> dict:
    total_holding_cost = 0
    total_stockout_cost = 0
    total_excess_value = 0
    total_shortage_value = 0
    sku_simulations = []

    for sku in imbalance_results:
        holding_cost = calculate_holding_cost(sku["excess_units"], sku["unit_cost"])
        stockout_cost = calculate_stockout_cost(sku["shortage_units"], sku["unit_cost"])

        total_holding_cost += holding_cost
        total_stockout_cost += stockout_cost
        total_excess_value += sku["excess_value"]
        total_shortage_value += sku["shortage_value"]

        sku_simulations.append({
            "sku_id": sku["sku_id"],
            "location": sku["location"],
            "status": sku["status"],
            "holding_cost": holding_cost,
            "stockout_cost": stockout_cost,
            "excess_value": sku["excess_value"],
            "shortage_value": sku["shortage_value"],
        })

    potential_savings = round(total_holding_cost * 0.6 + total_stockout_cost * 0.7, 2)

    return {
        "total_holding_cost": round(total_holding_cost, 2),
        "total_stockout_cost": round(total_stockout_cost, 2),
        "total_excess_value": round(total_excess_value, 2),
        "total_shortage_value": round(total_shortage_value, 2),
        "potential_savings": potential_savings,
        "working_capital_tied": round(total_excess_value, 2),
        "sku_simulations": sku_simulations,
    }