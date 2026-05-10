import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"

def call_claude(system_prompt: str, user_message: str, max_tokens: int = 1500) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text

DIAGNOSIS_SYSTEM_PROMPT = """You are an expert inventory analyst. You will be given data about 
overstocked and understocked SKUs across warehouse locations. Your job is to identify the most 
likely root causes of inventory imbalance. Be specific, concise, and data-driven. 
Return your analysis as plain text with clear sections."""

RECOMMENDATION_SYSTEM_PROMPT = """You are a supply chain optimization expert. Based on the 
inventory calculations provided, generate specific, actionable recommendations for safety stock 
levels, reorder points, and inter-location transfers. Be precise and reference the actual SKU 
data. Return a JSON array of recommendation strings."""

REPORT_SYSTEM_PROMPT = """You are a senior supply chain consultant writing for a C-suite audience. 
Generate a concise executive summary of the inventory optimization analysis. Include: key findings, 
financial impact, top 3 priority actions, and expected outcomes. Use professional business language. 
Format with clear sections using markdown headers."""

def diagnose_inventory(imbalance_data: list[dict], summary: dict) -> str:
    user_message = f"""
Inventory Summary:
- Total SKUs: {summary['total_skus']}
- Overstocked: {summary['overstocked_count']}
- Understocked: {summary['understocked_count']}
- Critically understocked: {summary['critical_count']}
- Total excess value: ${summary['total_excess_value']:,.2f}
- Total shortage value: ${summary['total_shortage_value']:,.2f}

Top imbalanced SKUs:
{format_sku_data(imbalance_data[:10])}

Diagnose the root causes of these inventory imbalances.
"""
    return call_claude(DIAGNOSIS_SYSTEM_PROMPT, user_message)

def generate_recommendations(imbalance_data: list[dict], financial: dict) -> str:
    user_message = f"""
Financial Impact:
- Total holding cost: ${financial['total_holding_cost']:,.2f}
- Total stockout cost: ${financial['total_stockout_cost']:,.2f}
- Potential savings: ${financial['potential_savings']:,.2f}

SKU Data:
{format_sku_data(imbalance_data[:15])}

Generate specific recommendations as a JSON array of strings.
"""
    return call_claude(RECOMMENDATION_SYSTEM_PROMPT, user_message)

def generate_report(summary: dict, financial: dict, diagnosis: str, recommendations: str) -> str:
    user_message = f"""
Inventory Analysis Results:

SUMMARY:
{summary}

FINANCIAL IMPACT:
{financial}

ROOT CAUSE DIAGNOSIS:
{diagnosis}

RECOMMENDATIONS:
{recommendations}

Write the executive summary report.
"""
    return call_claude(REPORT_SYSTEM_PROMPT, user_message, max_tokens=2000)

def format_sku_data(skus: list[dict]) -> str:
    lines = []
    for sku in skus:
        lines.append(
            f"- SKU {sku.get('sku_id')} @ {sku.get('location')}: "
            f"status={sku.get('status')}, "
            f"current={sku.get('current_stock')}, "
            f"reorder_point={sku.get('reorder_point')}, "
            f"excess_value=${sku.get('excess_value', 0):,.2f}"
        )
    return "\n".join(lines)
