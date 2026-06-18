The Build Journey: Engineering a Full-Stack RAG Pipeline

This document serves as an exact record of the development process, architectural decisions, and the intense debugging journey I went through to build this dynamic Retrieval-Augmented Generation (RAG) application from scratch.

Phase 1: Architectural Design & Modularization

Instead of writing a monolithic script, I deliberately separated the backend logic into a clean, enterprise-grade src/ directory.

loader.py & splitter.py: Configured to ingest PDFs and cleanly chop them into 1000-character chunks with 200-character overlaps.

embeddings.py: Swapped legacy tools for the modern langchain-huggingface package, utilizing the lightweight all-MiniLM-L6-v2 model.

vectorstore.py: Set up ChromaDB to run ephemerally (in-memory). This was a crucial architectural decision to ensure the app remains stateless between sessions and doesn't eat up disk space on cloud deployments.

rag_chain.py: Wired the vector database up to Google's Gemini 1.5 Flash using LangChain Expression Language (LCEL).

Phase 2: The Dependency Wars

Once the modules were wired into FastAPI (app.py), the environment debugging began.

Conflict 1: The Protobuf Clash: Installing the LangChain Google integration brought in protobuf 6.33.2, which triggered errors against an existing local tensorflow environment (which demanded protobuf<6.0.0). I safely ignored this for the RAG app, noting that a downgrade to 5.x would patch it globally if needed.

Conflict 2: The Missing Neural Network (NameError 'nn' is not defined): The Hugging Face transformers library crashed upon startup. I diagnosed this as an out-of-sync local PyTorch installation and executed a forced upgrade: pip install torch accelerate transformers --upgrade.

Conflict 3: Breaking Computer Vision: Upgrading PyTorch to 2.12.0 triggered dependency warnings for existing facenet-pytorch and torchvision libraries. I made the engineering decision to ignore these warnings, correctly identifying that my text-based RAG pipeline did not rely on those vision libraries.

Phase 3: The Windows "Boss Fights"

Running a complex AI application on local Windows environments introduced a series of highly specific OS-level bugs that required immediate patching.

Boss 1: The Emoji Crash (UnicodeEncodeError)

The Bug: The server crashed immediately during the startup event with UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680'.

The Diagnosis: The Windows terminal (cp1252 encoding) panicked when my Python logger tried to print a rocket emoji (🚀).

The Fix: Removed the emoji from the console print statement and updated the logger.py RotatingFileHandler to explicitly use encoding="utf-8" to prevent future crashes when reading complex PDF text.

Boss 2: The Hot-Reload Crash (forrtl: error (200))

The Bug: The server booted, but crashed with a severe libifcoremd.dll error whenever an endpoint was hit.

The Diagnosis: I identified a known architectural bug where the C++ backends of PyTorch and NumPy clash with Uvicorn's --reload (WatchFiles) threading on Windows, causing a false Control-C abort sequence.

The Fix: Disabled hot-reloading (uvicorn app:app), which completely stabilized the server memory.

Boss 3: The File System Collision (WinError 183)

The Bug: Uploading a PDF triggered FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'data'.

The Diagnosis: I had written os.makedirs("data", exist_ok=True). However, a local file named data (no extension) already existed in the directory. Windows threw a fatal error because it couldn't create a folder with the same name as a file.

The Fix: Refactored the temp-file routing to use a highly specific temp_uploads/ directory, permanently bypassing the collision.

Phase 4: The Phantom Cache

The Bug: The pipeline failed midway through processing with ImportError: Could not import sentence_transformers. However, running pip install returned "Requirement already satisfied".

The Diagnosis: A network timeout earlier in the build process had created the sentence-transformers folder in the pip cache, but failed to download the actual code. Pip was being tricked by an empty folder.

The Fix: Used the "sledgehammer" command: pip install --force-reinstall --no-cache-dir sentence-transformers to bypass the corrupted local cache and force a fresh binary download. This successfully unblocked the embedding pipeline.

Phase 5: The "No-React" Full-Stack Pivot

With the backend fully operational, I needed a frontend. Instead of context-switching to a completely different language and framework (React) and managing two separate servers, I engineered an all-in-one solution.

I wrote a beautiful, single-page Vanilla HTML/JS frontend styled with Tailwind CSS.

I embedded it directly into the FastAPI application using HTMLResponse.

This allowed me to serve a complete, professional web application from a single Python server, drastically simplifying the deployment process.

Conclusion

This build journey evolved from writing simple Python scripts to engineering a robust, modular microservice architecture. By systematically hunting down and resolving complex OS-level threading issues, file system quirks, and corrupted dependency caches, I successfully delivered a production-ready AI application.