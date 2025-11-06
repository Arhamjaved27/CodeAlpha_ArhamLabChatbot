from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    confidence: float
    matched_question: Optional[str] = None
    category: Optional[str] = None


class FAQ(BaseModel):
    """FAQ data model"""
    id: int
    question: str
    answer: str
    category: Optional[str] = None

