"""Parser Agent - Extracts structured task from natural language using LLM"""

from typing import Dict, Any
from utils.logger import app_logger
from tools.gemini_tools import gemini_service

class ParserAgent:
    """Extracts structured task data from unstructured text"""
    
    async def extract_task_structure(self, text: str) -> Dict[str, Any]:
        """
        Use LLM to extract task structure
        Returns: {title, description, priority, due_date, labels}
        """
        app_logger.info(f"Extracting structure from: {text[:80]}...")
        
        task = gemini_service.extract_task_structure(text)
        
        # Ensure required fields
        task.setdefault("title", text[:50])
        task.setdefault("description", text)
        task.setdefault("priority", 1)
        task.setdefault("due_date", None)
        task.setdefault("labels", [])
        
        app_logger.info(f"Extracted task: {task['title']}")
        return task

parser_agent = ParserAgent()
