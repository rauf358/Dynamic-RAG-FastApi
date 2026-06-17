from langchain_huggingface import HuggingFaceEmbeddings
from src.logger import logger

def get_embeddings(model_name: str = "all-MiniLM-L6-v2"):
    """
    Initializes and returns the HuggingFace embedding model.
    This model translates text chunks into mathematical vectors.
    """
    logger.info(f"Initializing embedding model: {model_name}")
    
    try:
        # Initialize the HuggingFace embeddings model
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        logger.info("Successfully loaded embedding model.")
        
        # Return the embedding object so ChromaDB can use it
        return embeddings
        
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {str(e)}", exc_info=True)
        raise e