import uuid
import json
import os
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import StringIO
from models.schemas import UploadResponse

router = APIRouter()

REQUIRED_COLUMNS = {
    "sku_id", "location", "current_stock", "avg_daily_demand",
    "demand_std_dev", "lead_time_days", "lead_time_std_dev", "unit_cost"
}

SESSIONS_DIR = "/tmp/sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def save_session(session_id: str, data: list):
    with open(f"{SESSIONS_DIR}/{session_id}.json", "w") as f:
        json.dump(data, f)

def get_session(session_id: str) -> list:
    path = f"{SESSIONS_DIR}/{session_id}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Session not found. Please upload a CSV first.")
    with open(path, "r") as f:
        return json.load(f)

@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    contents = await file.read()
    try:
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing required columns: {', '.join(sorted(missing))}")
    df = df.dropna(subset=list(REQUIRED_COLUMNS))
    session_id = str(uuid.uuid4())
    save_session(session_id, df.to_dict(orient="records"))
    return UploadResponse(
        session_id=session_id,
        rows_parsed=len(df),
        columns_found=list(df.columns),
        preview=df.head(5).to_dict(orient="records")
    )
