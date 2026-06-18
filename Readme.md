Dynamic RAG Engine 🚀

A full-stack, ephemeral Retrieval-Augmented Generation (RAG) API built with FastAPI, LangChain, and Google's Gemini 1.5 Flash.

This application allows users to upload PDF documents dynamically, vectorizes the text in real-time using local Hugging Face embeddings, and serves a chat interface to query the document using an LLM.

🏗️ Architecture

Backend Framework: FastAPI (Asynchronous, High-Performance)

Orchestration: LangChain

Embedding Model: all-MiniLM-L6-v2 (via Hugging Face)

Vector Database: ChromaDB (Ephemeral / In-Memory for session security)

LLM: Google Gemini 1.5 Flash

Frontend: Vanilla HTML/JS with Tailwind CSS (Served via FastAPI)

✨ Features

Zero-Footprint DB: Uses an in-memory ChromaDB instance that wipes clean after the session, ensuring data privacy and saving server storage.

Modular Pipeline: Document loading, text splitting, embedding, and chain building are separated into clean, maintainable micro-modules (src/).

Custom Logging: Built-in rotating file loggers and middleware for precise API request tracing.

Integrated UI: A modern, single-page application built directly into the root API endpoint.

🚀 Quick Start (Local Deployment)

1. Clone the repository

git clone [https://github.com/yourusername/dynamic-rag-fastapi.git](https://github.com/yourusername/dynamic-rag-fastapi.git)
cd dynamic-rag-fastapi


2. Install dependencies

It is recommended to use a virtual environment.

pip install -r requirements.txt


3. Set your Environment Variables

Create a .env file in the root directory or export the variable in your terminal:

export GOOGLE_API_KEY="your_gemini_api_key_here"


4. Run the Server

Note for Windows users: Avoid using --reload to prevent Uvicorn threading clashes with local PyTorch installations.

uvicorn app:app


5. Access the App

Web UI: http://127.0.0.1:8000/

Interactive API Docs (Swagger): http://127.0.0.1:8000/docs

📡 API Endpoints

GET /: Serves the frontend web interface.

POST /upload: Accepts a multipart/form-data PDF, chunks the text, creates embeddings, and initializes the RAG chain.

POST /chat: Accepts a JSON payload {"message": "string"} and returns the LLM's context-aware response.