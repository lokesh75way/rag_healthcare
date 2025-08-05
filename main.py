from fastapi import FastAPI, Request
from pydantic import BaseModel
from uuid import uuid4
from agents.langchain_agent import handle_user_message

app = FastAPI()

# Memory store: session_id -> chat_history
session_store = {}

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

@app.post("/test")
async def test(request: Request):
    body = await request.body()
    print(body)  # This will print raw bytes
    return {}

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    message = request.message

    # Get or create chat history
    history = session_store.get(session_id, [])
    
    print(history)
    
    # Call LangChain agent
    reply = await handle_user_message(message, history)

    # Update chat history dynamically
    history.append((reply['input'], reply['output']))
    session_store[session_id] = history

    return {
        "session_id": session_id,
        "reply": reply
    }