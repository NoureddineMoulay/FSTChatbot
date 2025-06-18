import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import the main conversational RAG chain from your retrieval.py script
# Make sure retrieval.py is in the same directory or accessible via Python path
from retrieval import conversational_rag_chain # This is the chain that includes history and RAG logic

import logging

logger = logging.getLogger("uvicorn.error")

# --- FastAPI application setup ---
app = FastAPI(
    title="FST Marrakech Chatbot API",
    description="API for the FST Marrakech RAG Chatbot with temporary session history.",
    version="1.0.0",
)

# --- CORS Middleware ---
# This is crucial for allowing your frontend (running on a different origin/port)
# to make requests to this backend API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. In production, specify your frontend's origin(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models for Request and Response ---

class ChatRequest(BaseModel):
    """
    Request model for the chatbot.
    `question`: The user's query.
    `session_id`: A unique ID for the user's session (e.g., from browser localStorage).
                  This is used to maintain temporary conversation history.
    """
    question: str
    session_id: str # Crucial for identifying the user's temporary session

class ChatResponse(BaseModel):
    """
    Response model for the chatbot.
    `answer`: The chatbot's response.
    """
    answer: str

# --- API Endpoint ---

@app.post("/chat", response_model=ChatResponse) # Changed endpoint to /chat for clarity
async def chat_endpoint(request: ChatRequest):
    """
    Handles user queries, retrieves information from FST Marrakech documents,
    and maintains temporary conversation history for the session.
    """
    try:
        # Invoke the conversational_rag_chain.
        # The `config` dictionary is used to pass the session_id to `RunnableWithMessageHistory`
        # which then uses it to get/create the correct in-memory history.
        response = conversational_rag_chain.invoke(
            {"input": request.question}, # The input key must match `input_messages_key` in RunnableWithMessageHistory
            config={"configurable": {"session_id": request.session_id}}
        )
        
        # The 'answer' key is the default output of create_retrieval_chain
        # when it passes through document_combiner_chain and the final RunnableLambda.
        assistant_response_text = response["answer"]
        
        return ChatResponse(answer=assistant_response_text)
    except Exception as e:
        logger.error(f"Error processing chat request for session {request.session_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

# --- Health Check Endpoint (Optional but Recommended) ---
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to ensure the API is running.
    """
    return {"status": "ok", "message": "FST Marrakech Chatbot API is running."}

# To run this API:
# 1. Save this file as `main.py` (or `app.py`)
# 2. Open your terminal in the `backend` directory
# 3. Run: `uvicorn main:app --reload --port 8001`
#    (Use `main:app` if your file is `main.py`, `app:app` if `app.py`)
# `--reload` is useful for development; remove it for production.