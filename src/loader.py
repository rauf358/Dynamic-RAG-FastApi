from langchain_community.document_loaders import PyPDFLoader
from src.logger import logger

def load_pdf(file_path: str):
    """
    Loads a PDF file from the given path and returns a list of LangChain Document objects.
    """
    logger.info(f"Attempting to load PDF from: {file_path}")
    try:
        # Initialize the loader
        loader = PyPDFLoader(file_path)
        
        # Load the document
        docs = loader.load()
        
        logger.info(f"Successfully loaded {len(docs)} pages from the PDF.")
        
        # Return the docs so the splitter can use them
        return docs
        
    except Exception as e:
        logger.error(f"PDF Loader failed to read {file_path}: {str(e)}", exc_info=True)
        raise e