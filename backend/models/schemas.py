from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SKUStatus(str, Enum):
    overstocked = "overstocked"
    understocked = "understocked"
    critically_understocked = "critically_understocked"
    healthy = "healthy"

class SKUInput(BaseModel):
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

class SKUResult(BaseModel):
    sku_id: str
    location: str
    current_stock: float
    safety_stock: float
    reorder_point: float
    eoq: float
    max_stock: float
    days_of_stock: float
    avg_daily_demand: float
    unit_cost: float
    status: SKUStatus
    excess_units: float
    shortage_units: float
    excess_value: float
    shortage_value: float

class FinancialSummary(BaseModel):
    total_holding_cost: float
    total_stockout_cost: float
    total_excess_value: float
    total_shortage_value: float
    potential_savings: float
    working_capital_tied: float

class InventorySummary(BaseModel):
    total_skus: int
    overstocked_count: int
    understocked_count: int
    critical_count: int
    healthy_count: int
    total_excess_value: float
    total_shortage_value: float

class AnalysisResponse(BaseModel):
    session_id: str
    summary: InventorySummary
    financial: FinancialSummary
    skus: list[SKUResult]
    diagnosis: Optional[str] = None
    recommendations: Optional[list[str]] = None
    report: Optional[str] = None

class UploadResponse(BaseModel):
    session_id: str
    rows_parsed: int
    columns_found: list[str]
    preview: list[dict]