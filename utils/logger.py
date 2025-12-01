import logging
import json
from datetime import datetime
from typing import Any, Dict
import os

class JSONFormatter(logging.Formatter):
    """Format logs as structured JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra_data"):
            log_obj.update(record.extra_data)
        
        return json.dumps(log_obj, default=str)

def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """Setup structured logging"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Console handler
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    return logger

# Main application logger
app_logger = setup_logging("TaskFlow", os.getenv("LOG_LEVEL", "INFO"))
