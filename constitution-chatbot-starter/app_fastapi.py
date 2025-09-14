from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from rag_pipeline import RAGBot

load_dotenv()

app = FastAPI(title="Constitution Chatbot API", version="1.0.0")

# Allow all origins for simplicity (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

# Initialize on startup so we don't rebuild on every call
@app.on_event("startup")
def startup():
    global BOT
    pdf_path = os.getenv("PDF_PATH", "data/constitution.pdf")
    api_key = os.getenv("GOOGLE_API_KEY")
    BOT = RAGBot(pdf_path=pdf_path, google_api_key=api_key)

@app.post("/ask")
def ask(data: Query):
    return BOT.ask(data.question)
