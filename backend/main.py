from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, analyze, report

app = FastAPI(
    title="Inventory Intelligence Engine",
    description="Multi-agent inventory optimization API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(report.router, prefix="/api", tags=["Report"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Inventory Intelligence Engine is running"}