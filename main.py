"""
ResQ AI - Emergency Resource Locator
Backend: FastAPI + Endee Vector Database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from app.endee_client import EndeeClient
from app.seed_data import EMERGENCY_RESOURCES

app = FastAPI(
    title="ResQ AI - Emergency Resource Locator",
    description="AI-powered emergency resource finder using Endee Vector Database",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

endee = EndeeClient()

# ── Models ──
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    resource_type: Optional[str] = None  # hospital, police, fire, blood, ambulance, shelter

class SearchResult(BaseModel):
    id: str
    name: str
    type: str
    address: str
    phone: str
    distance_km: float
    is_open: bool
    similarity_score: float
    icon: str

# ── Startup ──
@app.on_event("startup")
async def startup():
    """Initialize Endee index and seed emergency data on startup."""
    print("🚀 Starting ResQ AI...")
    await endee.initialize()
    await endee.seed_resources(EMERGENCY_RESOURCES)
    print("✅ Endee Vector DB ready with emergency resources!")

# ── Routes ──
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ResQ AI", "vector_db": "Endee"}

@app.post("/api/search", response_model=list[SearchResult])
async def search_resources(req: SearchRequest):
    """
    Semantic search for emergency resources using Endee vector DB.
    Converts query to embedding, then finds nearest vectors.
    """
    try:
        results = await endee.search(
            query=req.query,
            top_k=req.top_k,
            resource_type=req.resource_type
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resources")
async def get_all_resources():
    """Return all indexed emergency resources."""
    return EMERGENCY_RESOURCES

@app.get("/api/resources/{resource_type}")
async def get_by_type(resource_type: str):
    """Return resources filtered by type."""
    filtered = [r for r in EMERGENCY_RESOURCES if r["type"] == resource_type]
    if not filtered:
        raise HTTPException(status_code=404, detail=f"No resources found for type: {resource_type}")
    return filtered

@app.get("/api/stats")
async def get_stats():
    """Return vector DB stats."""
    return await endee.get_stats()