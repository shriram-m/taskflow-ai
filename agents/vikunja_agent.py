"""Vikunja Agent - Creates tasks in Vikunja via REST API"""

from typing import Dict, Any, Optional
from utils.logger import app_logger
from tools.vikunja_api import create_vikunja_client
from utils.memory import SessionMemory
import asyncio

class VikunjaBAgent:
    """Handles task creation in Vikunja"""
    
    def __init__(self, memory: SessionMemory):
        self.memory = memory
        self.vikunja_client = create_vikunja_client()
        self._initialized = False
    
    async def initialize(self) -> bool:
        """Initialize Vikunja connection"""
        if self._initialized:
            return True
        
        try:
            if not self.vikunja_client.test_connection():
                app_logger.error("Vikunja connection test failed")
                return False
            
            if not self.vikunja_client.authenticate():
                app_logger.error("Vikunja authentication failed")
                return False
            
            self._initialized = True
            app_logger.info("Vikunja agent initialized")
            return True
        
        except Exception as e:
            app_logger.error(f"Vikunja init error: {e}")
            return False
    
    async def create_task(self, task: Dict[str, Any], source_type: str = "text") -> Dict[str, Any]:
        """Create task in Vikunja"""
        try:
            app_logger.info(f"Creating task in Vikunja: {task.get('title')} from source '{source_type}'")
            
            # Pass source_type for color coding
            result = await asyncio.to_thread(
                self.vikunja_client.create_task,
                title=task.get("title", ""),
                description=task.get("description", ""),
                priority=task.get("priority", 1),
                due_date=task.get("due_date"),
                labels=task.get("labels", []),
                source_type=source_type
            )
            
            return result
        except Exception as e:
            app_logger.error(f"Error creating task in Vikunja: {e}")
            raise

class VikunjaBAgentFactory:
    @staticmethod
    def create(memory: SessionMemory) -> VikunjaBAgent:
        return VikunjaBAgent(memory)
