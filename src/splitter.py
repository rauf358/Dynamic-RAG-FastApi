from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import logger

def split_text(docs, chunk_size=1000, chunk_overlap=200):
    """
    Takes a list of LangChain Document objects and splits them into smaller, 
    manageable chunks for the vector database.
    """
    logger.info(f"Starting text splitting: chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    try:
        # Initialize the LangChain text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""] # Splits by paragraph, then line, then word
        )
        
        # Split the documents
        chunks = text_splitter.split_documents(docs)
        
        logger.info(f"Successfully split the document into {len(chunks)} individual chunks.")
        
        # Return the chunks so the embedding model can vectorize them
        return chunks
        
    except Exception as e:
        logger.error(f"Text splitting failed: {str(e)}", exc_info=True)
        raise e