"""Enricher Agent - Adds context and intelligence to extracted tasks"""

from typing import Dict, Any
from utils.logger import app_logger
from tools.gemini_tools import gemini_service
from utils.memory import SessionMemory

class EnricherAgent:
    """Enhances tasks with context and learning"""
    
    def __init__(self, memory: SessionMemory):
        self.memory = memory
    
    async def enrich_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance task using context and patterns
        - Infer priority from keywords
        - Suggest labels
        - Learn from user patterns
        """
        app_logger.info(f"Enriching task: {task['title']}")
        
        # Get context from memory
        context = self.memory.get_context(limit=5)
        patterns = self.memory.get_user_patterns()
        
        context_str = f"{context}\nUser patterns: {patterns}"
        
        # Use LLM to enhance
        enriched_task = gemini_service.enrich_task(task, context_str)
        
        app_logger.info(f"Enriched task priority: {enriched_task.get('priority')}")
        return enriched_task

class EnricherAgentFactory:
    @staticmethod
    def create(memory: SessionMemory) -> EnricherAgent:
        return EnricherAgent(memory)
