import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.travel import TravelRequest, TravelResponse

app = FastAPI(
    title="AgentAtlas API",
    description="Multi-Agent Travel Planner Backend",
    version="0.1.0",
)

# Enable CORS for frontend (e.g. Next.js / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "AgentAtlas API is running"
    }


@app.post("/api/travel", response_model=TravelResponse)
async def travel_planner(request: TravelRequest):
    # Placeholder for workflow execution
    return TravelResponse(
        reply=f"Received query: '{request.message}'. AgentAtlas workflow will process this.",
        thread_id=request.thread_id or "default-thread"
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
