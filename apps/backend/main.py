from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.travel import TravelRequest, TravelResponse
from workflows import run_travel_workflow
from tools.mcp_client import close_mcp_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    yield
    # Clean shutdown of MCP resources and processes
    await close_mcp_client()


app = FastAPI(
    title="AgentAtlas API",
    description="Multi-Agent Travel Planner Backend",
    version="0.1.0",
    lifespan=lifespan,
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
        "message": "AgentAtlas API is running",
    }


@app.post("/api/travel", response_model=TravelResponse)
async def travel_planner(request: TravelRequest):
    thread_id = request.thread_id or "default-thread"
    result = await run_travel_workflow(user_query=request.message, thread_id=thread_id)
    return TravelResponse(
        reply=result.get("itinerary", "No itinerary generated"),
        thread_id=thread_id,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
