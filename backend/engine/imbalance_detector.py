from engine.inventory_calculator import SKUMetrics, run_calculations

OVERSTOCK_THRESHOLD = 1.5
UNDERSTOCK_THRESHOLD = 0.5

def classify_sku(calc: dict) -> str:
    current = calc["current_stock"]
    max_stock = calc["max_stock"]
    reorder_point = calc["reorder_point"]
    safety_stock = calc["safety_stock"]

    if current > max_stock * OVERSTOCK_THRESHOLD:
        return "overstocked"
    elif current <= safety_stock:
        return "critically_understocked"
    elif current <= reorder_point:
        return "understocked"
    else:
        return "healthy"

def calculate_excess_units(calc: dict) -> float:
    excess = calc["current_stock"] - calc["max_stock"]
    return round(max(excess, 0), 2)

def calculate_shortage_units(calc: dict) -> float:
    shortage = calc["reorder_point"] - calc["current_stock"]
    return round(max(shortage, 0), 2)

def detect_imbalances(sku_metrics_list: list[SKUMetrics]) -> list[dict]:
    results = []

    for metrics in sku_metrics_list:
        calc = run_calculations(metrics)
        status = classify_sku(calc)
        excess_units = calculate_excess_units(calc)
        shortage_units = calculate_shortage_units(calc)
        excess_value = round(excess_units * metrics.unit_cost, 2)
        shortage_value = round(shortage_units * metrics.unit_cost, 2)

        results.append({
            **calc,
            "status": status,
            "excess_units": excess_units,
            "shortage_units": shortage_units,
            "excess_value": excess_value,
            "shortage_value": shortage_value,
        })

    return results

def get_summary(imbalance_results: list[dict]) -> dict:
    total = len(imbalance_results)
    overstocked = [r for r in imbalance_results if r["status"] == "overstocked"]
    understocked = [r for r in imbalance_results if r["status"] == "understocked"]
    critical = [r for r in imbalance_results if r["status"] == "critically_understocked"]
    healthy = [r for r in imbalance_results if r["status"] == "healthy"]

    return {
        "total_skus": total,
        "overstocked_count": len(overstocked),
        "understocked_count": len(understocked),
        "critical_count": len(critical),
        "healthy_count": len(healthy),
        "total_excess_value": round(sum(r["excess_value"] for r in overstocked), 2),
        "total_shortage_value": round(sum(r["shortage_value"] for r in understocked + critical), 2),
    }