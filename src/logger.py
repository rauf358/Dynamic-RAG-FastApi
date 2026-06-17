import logging
import sys
from logging.handlers import RotatingFileHandler
import os

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def setup_logger():
    # 1. Create a custom logger
    logger = logging.getLogger("rag_app")
    logger.setLevel(logging.DEBUG) # Capture everything from DEBUG and above

    # Avoid duplicate logs if this function is called multiple times
    if logger.handlers:
        return logger

    # 2. Create formatting (How the log looks)
    # Example: 2026-06-17 10:45:01,123 - INFO - rag_app - Something happened
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # 3. Console Handler (Prints to your terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # Keep console clean (INFO, WARNING, ERROR)
    console_handler.setFormatter(formatter)

    # 4. File Handler (Saves to logs/app.log)
    # Auto-rotates when the file hits 5MB, keeps 3 backups max
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG) # Save EVERYTHING to the file
    file_handler.setFormatter(formatter)

    # 5. Add handlers to our logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create a globally accessible logger object
logger = setup_logger()