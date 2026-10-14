from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import shutil

from fastapi.middleware.cors import CORSMiddleware

from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.ingestion_service import IngestionService
from backend.app.services.llm_service import LLMService


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Support Docs Copilot",
    description="AI-powered support documentation assistant",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Initialize Services
# --------------------------------------------------

retrieval_service = RetrievalService()
ingestion_service = IngestionService()
llm_service = LLMService()


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class AskRequest(BaseModel):
    question: str


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Support Docs Copilot API is running"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Upload Document
# --------------------------------------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    upload_dir = Path("uploads")

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_dir / file.filename

    # Save uploaded file
    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Ingest document
    result = ingestion_service.ingest_document(
        str(file_path)
    )

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "chunks": result["chunks"],
        "embedding_dimension": result["embedding_dimension"],
        "status": result["status"]
    }


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.post("/ask")
def ask_question(
    request: AskRequest
):

    # Retrieve relevant document context
    context = retrieval_service.get_context(
        query=request.question,
        top_k=5
    )

    # No relevant information found
    if not context:

        return {
            "question": request.question,
            "answer": (
                "I could not find relevant information "
                "in the uploaded documents."
            )
        }

    # Generate answer using Gemini
    try:

        answer = llm_service.generate_answer(
            question=request.question,
            context=context
        )

    except Exception as e:

        print(f"LLM Error: {e}")

        return {
            "question": request.question,
            "answer": (
                "The AI model is temporarily unavailable. "
                "Please try again in a moment."
            )
        }

    # Return final answer
    return {
        "question": request.question,
        "answer": answer
    }