from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import time

# 1. Import our custom modules from the src/ folder
from src.logger import logger
from src.loader import load_pdf
from src.splitter import split_text
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.rag_chain import build_chain
from fastapi.responses import HTMLResponse
# 2. Initialize FastAPI
app = FastAPI(title="Dynamic PDF RAG API")

# Allow frontend applications (like React) to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# AUTO-LOGGING MIDDLEWARE
# ==========================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Completed {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
    return response

# ==========================================
# GLOBAL STATE & MODELS
# ==========================================
class ChatRequest(BaseModel):
    message: str

# This holds our LangChain pipeline in memory for the active session
current_chain = None

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Dynamic RAG API Server...")

# ==========================================
# API ENDPOINTS
# ==========================================
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Accepts a PDF, processes it through the RAG pipeline, and readies the chat."""
    global current_chain
    logger.info(f"Received file upload: {file.filename}")
    
    # 1. Save the file temporarily in a specific uploads folder
    upload_dir = "temp_uploads"
    temp_file_path = f"{upload_dir}/{file.filename}"
    
    # Create the directory safely
    os.makedirs(upload_dir, exist_ok=True)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info("Starting document processing pipeline...")
        
        # 2. THE PIPELINE EXECUTES HERE
        docs = load_pdf(temp_file_path)
        chunks = split_text(docs)
        embeddings = get_embeddings()
        vectorstore = create_vectorstore(chunks, embeddings)
        current_chain = build_chain(vectorstore)
        
        logger.info(f"Successfully processed {file.filename} and activated RAG chain.")
        return {"status": "success", "message": f"{file.filename} processed! You can now chat."}
    
    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    
    finally:
        # 3. Clean up the temporary PDF file to save server space
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.debug(f"Cleaned up temporary file: {temp_file_path}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Answers questions based on the currently uploaded PDF."""
    global current_chain
    
    if current_chain is None:
        logger.warning("User attempted to chat without uploading a PDF first.")
        raise HTTPException(status_code=400, detail="No PDF uploaded yet. Please upload a document first.")
    
    try:
        logger.info(f"User asked: '{request.message}'")
        answer = current_chain.invoke(request.message)
        logger.debug("Successfully generated LLM response.")
        return {"reply": answer}
    except Exception as e:
        logger.error(f"Error during chat generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

