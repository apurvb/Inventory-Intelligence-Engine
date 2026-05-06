<div align="center">

# 🏭 Inventory Intelligence Engine

### *Turn a spreadsheet into a boardroom-ready inventory strategy in 30 seconds*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Visit_App-6366f1?style=for-the-badge)](https://inventory-intelligence-engine.vercel.app)
[![Claude AI](https://img.shields.io/badge/AI-Claude_Sonnet-cc785c?style=for-the-badge)](https://anthropic.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_+_Vite-61DAFB?style=for-the-badge)](https://react.dev)
[![Status](https://img.shields.io/badge/Status-Live_in_Production-10b981?style=for-the-badge)](#)

<br/>

> Upload your inventory CSV → Get AI-powered diagnosis, financial impact, and executive recommendations in under 60 seconds.

<br/>

![Dashboard Preview](https://raw.githubusercontent.com/apurvb/Inventory-Intelligence-Engine/main/sample_data/preview.png)

</div>

---

## 🧠 The Problem It Solves

Most companies are flying blind on inventory. They have spreadsheets but no intelligence. They know *what* they have — but not *why* it's wrong, *what it's costing them*, or *exactly what to do about it*.

This tool closes that gap. Upload your inventory data and within 60 seconds you get:

| Before | After |
|--------|-------|
| Raw stock numbers in a spreadsheet | SKUs ranked by financial risk |
| No idea why imbalances exist | AI-diagnosed root causes per SKU |
| Gut-feel reorder decisions | Mathematically optimal safety stock + EOQ |
| No sense of financial impact | Exact dollar value tied up or at risk |
| Hours of analysis for a report | Executive summary in seconds |

---

## ⚡ See It In Action

**Input:** A CSV with 5 columns of inventory data

**Output in 60 seconds:**
---

## 🏗️ How It's Built

What makes this different from a simple AI chatbot is the **two-layer architecture** — deterministic math first, AI reasoning second.
YOUR CSV FILE
                         │
                         ▼
        ┌────────────────────────────────┐
        │      LAYER 1: MATH ENGINE       │
        │  (No AI — pure formulas)        │
        │                                 │
        │  • EOQ Formula                  │
        │  • Safety Stock (Z-score)       │
        │  • Reorder Point Calculation    │
        │  • Holding Cost Modeling        │
        │  • Stockout Cost Estimation     │
        └─────────────┬──────────────────┘
                      │
               Clean, validated
               financial numbers
                      │
                      ▼
        ┌────────────────────────────────┐
        │    LAYER 2: AI AGENT PIPELINE   │
        │    (Claude reasons over math)   │
        │                                 │
        │  Agent 1 → Detect imbalances   │
        │  Agent 2 → Diagnose causes     │
        │  Agent 3 → Recommend actions  │
        │  Agent 4 → Simulate P&L        │
        │  Agent 5 → Write exec report  │
        └─────────────┬──────────────────┘
                      │
                      ▼
        ┌────────────────────────────────┐
        │         DASHBOARD + REPORT      │
        │                                 │
        │  KPI Cards  │  Bar Charts       │
        │  SKU Table  │  Executive PDF    │
        └────────────────────────────────┘
**Why this matters:** The AI never sees raw CSV data. It only reasons over clean, pre-calculated numbers. This is how real enterprise software works — and it's what separates a production system from a prototype.

---

## 🤖 The 5-Agent Pipeline

Each agent has exactly one job:

| Agent | Job | Method |
|-------|-----|--------|
| 🔍 **Detection** | Flag SKUs outside safe thresholds | Deterministic math |
| 🧠 **Diagnosis** | Explain *why* imbalances exist | Claude API |
| 📋 **Recommendation** | Prescribe exact actions with units + $ | Claude API |
| 💰 **Simulation** | Calculate P&L impact of recommendations | Deterministic math |
| 📄 **Report** | Write C-suite executive summary | Claude API |

---

## 🛠️ Tech Stack
---

## 🚀 Run It Locally

### 1. Clone
```bash
git clone https://github.com/apurvb/Inventory-Intelligence-Engine.git
cd Inventory-Intelligence-Engine
```

### 2. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uvicorn main:app --reload
# → Running at http://localhost:8000
# → API docs at http://localhost:8000/docs
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
# → Running at http://localhost:5173
```

### 4. Test It
Upload `sample_data/sample_inventory.csv` and watch the 5-agent pipeline run live.

---

## 📂 CSV Format

```csv
sku_id,location,current_stock,avg_daily_demand,demand_std_dev,lead_time_days,lead_time_std_dev,unit_cost
SKU-001,Warehouse-A,5000,20,5,7,1,25.00
SKU-002,Warehouse-A,50,30,8,7,1,15.00
```

| Column | What It Means |
|--------|--------------|
| `sku_id` | Your product identifier |
| `location` | Warehouse or store name |
| `current_stock` | Units on hand right now |
| `avg_daily_demand` | Average units sold per day |
| `demand_std_dev` | How much demand varies day to day |
| `lead_time_days` | Days from order to delivery |
| `lead_time_std_dev` | How much lead time varies |
| `unit_cost` | Cost per unit in dollars |

---

## 📁 Project Structure
---

## 🔑 Key Design Decisions

**1. Math before AI** — All inventory calculations (EOQ, safety stock, reorder points) happen in Python before any Claude call. The AI reasons over validated numbers, not guesses.

**2. Agent specialization** — Each agent has one job and one prompt. This produces better output than one giant prompt trying to do everything.

**3. Session-based architecture** — CSV data is stored server-side by session ID. The frontend never holds raw data, keeping the API clean.

**4. Deterministic financial simulation** — The P&L impact calculation is pure math, not AI estimation. When we say "$32,667 in savings", it's a formula result, not a guess.

---

<div align="center">

**Built with FastAPI · React · Anthropic Claude · Deployed on Railway + Vercel**

[🚀 Try the Live Demo](https://inventory-intelligence-engine.vercel.app) · [📦 Sample CSV](sample_data/sample_inventory.csv)

</div>
