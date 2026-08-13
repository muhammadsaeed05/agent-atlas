from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    message: str = Field(..., description="The user prompt or travel planning query")
    thread_id: str | None = Field(default=None, description="Optional conversation/thread ID")


class TravelResponse(BaseModel):
    reply: str = Field(..., description="The agent's response")
    thread_id: str | None = Field(default=None, description="Thread ID for continuing the conversation")
