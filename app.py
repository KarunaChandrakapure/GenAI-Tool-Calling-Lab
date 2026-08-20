from fastapi import FastAPI
from pydantic import BaseModel
from tool_calling import ask_llm

app = FastAPI(
    title="GENAI Tool Calling Lab",
    description="AI assistant using OPENAI Tool Calling + MySQL",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    question : str

@app.get("/")    
def home():
    return {
        "message":"GENAI Tool Calling Lab is running"
    }
@app.post("/chat")
def chat(request:ChatRequest):
    answer = ask_llm(request.question)
    return{
        "question":request.question,
        "answer":answer
    }
