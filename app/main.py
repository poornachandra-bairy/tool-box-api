from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the LLM service
from app.services.llm_service import LLMService

app = FastAPI(
    title="Toolbox API",
    description="A simple text processing service with LLM integration",
    version="1.0.0"
)

# Initialize LLM service
llm_service = LLMService()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for maintaining context")
    system_prompt: Optional[str] = Field(
        "You are a helpful AI assistant.",
        description="System prompt to set the behavior of the assistant"
    )

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    """
    Chat endpoint that takes a user message and returns an AI response.
    """
    try:
        response = await llm_service.generate_response(
            prompt=chat_input.message,
            system_prompt=chat_input.system_prompt,
            reset_conversation=chat_input.conversation_id is None
        )
        return {
            "response": response,
            "conversation_id": chat_input.conversation_id or "new_conversation"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)