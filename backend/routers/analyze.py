from fastapi import APIRouter, HTTPException
from engine.inventory_calculator import SKUMetrics, run_calculations
from engine.imbalance_detector import detect_imbalances, get_summary
from engine.financial_simulator import simulate_financial_impact
from utils.claude_client import diagnose_inventory, generate_recommendations, generate_report
from models.schemas import AnalysisResponse
from routers.upload import get_session
import uuid
import json

router = APIRouter()

@router.post("/analyze/{session_id}", response_model=AnalysisResponse)
async def analyze_inventory(session_id: str):
    raw_data = get_session(session_id)

    sku_metrics_list = []
    for row in raw_data:
        try:
            metrics = SKUMetrics(
                sku_id=str(row["sku_id"]),
                location=str(row["location"]),
                current_stock=float(row["current_stock"]),
                avg_daily_demand=float(row["avg_daily_demand"]),
                demand_std_dev=float(row["demand_std_dev"]),
                lead_time_days=float(row["lead_time_days"]),
                lead_time_std_dev=float(row["lead_time_std_dev"]),
                unit_cost=float(row["unit_cost"]),
                holding_cost_rate=float(row.get("holding_cost_rate", 0.25)),
                service_level=float(row.get("service_level", 0.95)),
            )
            sku_metrics_list.append(metrics)
        except (KeyError, ValueError) as e:
            raise HTTPException(status_code=422, detail=f"Invalid row data: {str(e)}")

    imbalance_results = detect_imbalances(sku_metrics_list)
    summary = get_summary(imbalance_results)
    financial = simulate_financial_impact(imbalance_results)

    diagnosis = diagnose_inventory(imbalance_results, summary)

    try:
        recommendations_raw = generate_recommendations(imbalance_results, financial)
        clean = recommendations_raw.strip().replace("```json", "").replace("```", "")
        recommendations = json.loads(clean)
        if not isinstance(recommendations, list):
            recommendations = [recommendations_raw]
    except Exception:
        recommendations = [generate_recommendations(imbalance_results, financial)]

    report = generate_report(summary, financial, diagnosis, str(recommendations))

    from models.schemas import SKUResult, FinancialSummary, InventorySummary
    return AnalysisResponse(
        session_id=session_id,
        summary=InventorySummary(**summary),
        financial=FinancialSummary(**{
            k: v for k, v in financial.items() if k != "sku_simulations"
        }),
        skus=[SKUResult(**r) for r in imbalance_results],
        diagnosis=diagnosis,
        recommendations=recommendations,
        report=report,
    )