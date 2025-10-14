# src/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from . import llm_service

app = FastAPI(title="Stellar AI Coding Assistant API", version="2.0.0")

class ReviewRequest(BaseModel):
    code: str
    language: str
    intent: str

class ReviewResponse(BaseModel):
    report: str

class ChatRequest(BaseModel):
    code_context: str
    history: List[Dict[str, str]]
    language: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/review", response_model=ReviewResponse)
def get_full_review(request: ReviewRequest):
    """Endpoint for a full, one-shot code analysis."""
    try:
        report_text = llm_service.get_text_review(request.code, request.language, request.intent)
        if report_text and not report_text.isspace():
            return ReviewResponse(report=report_text)
        else:
            raise HTTPException(status_code=500, detail="AI analysis was inconclusive.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    """Endpoint for conversational follow-ups."""
    try:
        reply_text = llm_service.get_chat_response(request.code_context, request.history, request.language)
        if reply_text and not reply_text.isspace():
            return ChatResponse(reply=reply_text)
        else:
            raise HTTPException(status_code=500, detail="AI response was empty.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))