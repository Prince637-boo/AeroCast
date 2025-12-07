import logging
import sys
from datetime import datetime

def setup_logging():
    """Configure le système de logging"""
    
    # Format des logs
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(filename)s:%(lineno)d - %(message)s"
    )
    
    # Configuration du logger racine
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            # Optionnel: logging.FileHandler("orientation.log")
        ]
    )
    
    # Logger pour httpx (plus silencieux)
    logging.getLogger("httpx").setLevel(logging.WARNING)

