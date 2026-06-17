from langchain_chroma import Chroma
from src.logger import logger

def create_vectorstore(chunks, embeddings):
    """
    Takes the split text chunks and the embedding model,
    and builds an ephemeral (in-memory) ChromaDB vector store.
    """
    logger.info(f"Creating vector store for {len(chunks)} chunks...")
    
    try:
        # Initialize the Chroma vector store from the document chunks.
        # By omitting 'persist_directory', the database is built in-memory,
        # which is much faster and perfect for temporary session-based files.
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        
        logger.info("Successfully built Chroma vector store.")
        
        # Return the vectorstore so the RAG chain can use it as a retriever
        return vectorstore
        
    except Exception as e:
        logger.error(f"Failed to create vector store: {str(e)}", exc_info=True)
        raise e