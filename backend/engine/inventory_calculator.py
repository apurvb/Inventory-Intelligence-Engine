import math
from dataclasses import dataclass

@dataclass
class SKUMetrics:
    sku_id: str
    location: str
    current_stock: float
    avg_daily_demand: float
    demand_std_dev: float
    lead_time_days: float
    lead_time_std_dev: float
    unit_cost: float
    holding_cost_rate: float = 0.25
    service_level: float = 0.95

def get_z_score(service_level: float) -> float:
    z_scores = {0.90: 1.28, 0.95: 1.645, 0.98: 2.05, 0.99: 2.326}
    return z_scores.get(service_level, 1.645)

def calculate_safety_stock(metrics: SKUMetrics) -> float:
    z = get_z_score(metrics.service_level)
    demand_variability = (metrics.lead_time_days * metrics.demand_std_dev ** 2)
    lead_time_variability = (metrics.avg_daily_demand ** 2 * metrics.lead_time_std_dev ** 2)
    safety_stock = z * math.sqrt(demand_variability + lead_time_variability)
    return round(safety_stock, 2)

def calculate_reorder_point(metrics: SKUMetrics) -> float:
    avg_demand_during_lead_time = metrics.avg_daily_demand * metrics.lead_time_days
    safety_stock = calculate_safety_stock(metrics)
    return round(avg_demand_during_lead_time + safety_stock, 2)

def calculate_eoq(metrics: SKUMetrics, annual_demand: float, ordering_cost: float = 50.0) -> float:
    holding_cost_per_unit = metrics.unit_cost * metrics.holding_cost_rate
    if holding_cost_per_unit == 0 or annual_demand == 0:
        return 0
    eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
    return round(eoq, 2)

def calculate_max_stock(metrics: SKUMetrics, eoq: float) -> float:
    safety_stock = calculate_safety_stock(metrics)
    return round(safety_stock + eoq, 2)

def calculate_days_of_stock(metrics: SKUMetrics) -> float:
    if metrics.avg_daily_demand == 0:
        return float('inf')
    return round(metrics.current_stock / metrics.avg_daily_demand, 1)

def run_calculations(metrics: SKUMetrics) -> dict:
    annual_demand = metrics.avg_daily_demand * 365
    safety_stock = calculate_safety_stock(metrics)
    reorder_point = calculate_reorder_point(metrics)
    eoq = calculate_eoq(metrics, annual_demand)
    max_stock = calculate_max_stock(metrics, eoq)
    days_of_stock = calculate_days_of_stock(metrics)

    return {
        "sku_id": metrics.sku_id,
        "location": metrics.location,
        "current_stock": metrics.current_stock,
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,
        "eoq": eoq,
        "max_stock": max_stock,
        "days_of_stock": days_of_stock,
        "avg_daily_demand": metrics.avg_daily_demand,
        "unit_cost": metrics.unit_cost,
    }

