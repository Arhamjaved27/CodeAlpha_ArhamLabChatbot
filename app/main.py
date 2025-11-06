from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from app.models import ChatRequest, ChatResponse, FAQ
from app.chatbot import FAQChatbot

# Initialize FastAPI app
app = FastAPI(
    title="FAQ Chatbot",
    description="A simple FAQ chatbot using FastAPI, SpaCy, and TF-IDF",
    version="1.0.0"
)

# Initialize chatbot
try:
    chatbot = FAQChatbot()
except Exception as e:
    chatbot = None
    print(f"Warning: Could not initialize chatbot: {e}")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Initialize templates
templates = None
if os.path.exists(templates_path):
    templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the chat UI"""
    if templates is None:
        return HTMLResponse(content="<h1>Chatbot UI</h1><p>Templates directory not found.</p>")
    
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user question and return best matching FAQ answer
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available. Please check the FAQ data file."
        )
    
    try:
        response = chatbot.get_response(request.question)
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/api/faqs", response_model=list[FAQ])
async def get_faqs():
    """
    Get all FAQs (for debugging/testing)
    """
    if chatbot is None:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available."
        )
    
    return chatbot.faqs


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chatbot_initialized": chatbot is not None,
        "faq_count": len(chatbot.faqs) if chatbot else 0
    }

