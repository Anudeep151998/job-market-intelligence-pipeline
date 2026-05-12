import logging
import os

def get_logger(name):
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if the logger is initialized multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # 1. File Handler: Saves logs to logs/pipeline.log
        fh = logging.FileHandler('logs/pipeline.log')
        
        # 2. Console Handler: Shows logs in your terminal
        ch = logging.StreamHandler()
        
        # Create a professional format: Timestamp - Name - Level - Message
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger