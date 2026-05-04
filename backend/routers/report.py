from fastapi import APIRouter, HTTPException
from routers.upload import get_session

router = APIRouter()

analysis_store = {}

def save_analysis(session_id: str, result: dict):
    analysis_store[session_id] = result

@router.get("/report/{session_id}")
async def get_report(session_id: str):
    if session_id not in analysis_store:
        raise HTTPException(
            status_code=404,
            detail="No analysis found for this session. Run /analyze first."
        )
    result = analysis_store[session_id]
    return {
        "session_id": session_id,
        "report": result.get("report"),
        "recommendations": result.get("recommendations"),
        "summary": result.get("summary"),
        "financial": result.get("financial"),
    }