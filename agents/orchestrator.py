"""Root Orchestrator - Coordinates all agents (Framework-Agnostic)"""

import os
from typing import Dict, Any, Optional
from utils.logger import app_logger
from utils.memory import SessionMemory
from utils.tracing import setup_tracing, get_tracer
from .input_processor import input_processor_agent
from .parser_agent import parser_agent
from .enricher_agent import EnricherAgentFactory
from .vikunja_agent import VikunjaBAgentFactory

class TaskFlowOrchestrator:
    """Main orchestration agent - Framework agnostic (No ADK dependency)"""
    
    def __init__(self):
        self.memory = SessionMemory(
            ttl_seconds=int(os.getenv("SESSION_TTL_SECONDS", "3600")),
            max_items=int(os.getenv("MAX_MEMORY_ITEMS", "100"))
        )
        self.enricher_agent = EnricherAgentFactory.create(self.memory)
        self.vikunja_agent = VikunjaBAgentFactory.create(self.memory)
        self.tracer = setup_tracing("taskflow-ai")
        self._initialized = False
    
    async def initialize(self) -> bool:
        """Initialize orchestrator and all sub-components"""
        try:
            app_logger.info("Initializing TaskFlow Orchestrator...")
            
            # Initialize Vikunja connection
            if not await self.vikunja_agent.initialize():
                app_logger.warning("Vikunja not available - will run in demo mode")
            
            # Verify Gemini API key
            gemini_key = os.getenv("GEMINI_API_KEY")
            if not gemini_key:
                raise ValueError("GEMINI_API_KEY not set")
            
            self._initialized = True
            app_logger.info("TaskFlow Orchestrator initialized successfully")
            return True
        
        except Exception as e:
            app_logger.error(f"Initialization error: {e}")
            raise
    
    async def process_input(self, input_data: Any, input_type: str = "text") -> Dict[str, Any]:
        """Main processing pipeline"""
        
        if not self._initialized:
            await self.initialize()
        
        trace_span = self.tracer.start_as_current_span("process_input") if self.tracer else None
        
        try:
            app_logger.info(f"Processing {input_type} input")
            
            # Step 1: Input Processing
            normalized_text, detected_type = await input_processor_agent.detect_and_process(
                input_data, input_type
            )
            
            self.memory.add_interaction(input_type, normalized_text, detected_type)
            
            # Step 2: Task Extraction
            task = await parser_agent.extract_task_structure(normalized_text)
            
            # Step 3: Task Enrichment
            enriched_task = await self.enricher_agent.enrich_task(task)
            
            # Step 4: Task Creation in Vikunja
            created_task = await self.vikunja_agent.create_task(
                enriched_task,
                source_type=detected_type  # Use detected_type, not input_type!
            )
            
            result = {
                "success": True,
                "task_id": created_task.get("id") if created_task else -1,
                "title": enriched_task.get("title"),
                "source": detected_type,
                "priority": enriched_task.get("priority"),
                "labels": enriched_task.get("labels", [])
            }
            
            app_logger.info(f"Processing complete: {result}")
            return result
        
        except Exception as e:
            app_logger.error(f"Processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "source": input_type
            }
        
        finally:
            if trace_span:
                trace_span.end()
    
    def get_memory_context(self) -> Dict[str, Any]:
        """Get session memory state"""
        return self.memory.to_dict()
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        app_logger.info("Cleaning up TaskFlow Orchestrator")
