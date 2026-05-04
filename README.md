# Inventory Intelligence Engine

A multi-agent AI-powered inventory optimization system that detects imbalances, diagnoses root causes, and generates executive-ready reports.

## What It Does

1. **Detects** overstocked and understocked SKUs across warehouse locations
2. **Diagnoses** root causes using Claude AI agent reasoning
3. **Recommends** optimized safety stock, reorder points, and transfers
4. **Simulates** financial impact of recommendations
5. **Generates** executive-ready inventory optimization reports

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS + Recharts
- **Backend:** Python FastAPI
- **AI:** Anthropic Claude API (multi-agent orchestration)
- **Data:** CSV upload

## Architecture
## Getting Started

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 and upload `sample_data/sample_inventory.csv` to test.

## Sample Data

A sample CSV is provided in `sample_data/sample_inventory.csv`.

## Key Features

- Drag and drop CSV upload
- Real-time multi-agent analysis progress
- Financial impact dashboard with charts
- SKU-level detail table with status badges
- AI-generated executive report with priority recommendations
