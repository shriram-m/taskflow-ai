#!/usr/bin/env python3
"""
TaskFlow AI - Main Entry Point
Multi-channel task management system with ADK
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# IMPORTANT: Import config FIRST to load .env
from config import settings

import os
from typing import Optional

from agents.orchestrator import TaskFlowOrchestrator
from utils.logger import app_logger
from utils.tracing import setup_tracing

# Initialize tracing
setup_tracing("taskflow-ai-main")

async def main():
    """Main workflow"""
    
    app_logger.info("=" * 60)
    app_logger.info("🚀 TaskFlow AI - Multi-Channel Task Management")
    app_logger.info("=" * 60 + "\n")
    
    try:
        # Initialize orchestrator
        orchestrator = TaskFlowOrchestrator()
        await orchestrator.initialize()
    
        # Sample inputs with proper format
        sample_inputs = [
            {
                "type": "text",
                "content": "Fix the login bug by Friday - it's critical"
            },
            {
                "type": "text",  # Set as text, but will auto-detect as email!
                "content": """From: manager@company.com
To: you@company.com
Subject: Review Q1 Marketing Presentation

Body: Hi, can you review the Q1 marketing presentation by end of week? 
It's needed for the board meeting."""
            },
            {
                "type": "text",
                "content": "Schedule team sync about new API design"
            }
        ]
    
        for i, input_item in enumerate(sample_inputs, 1):
            try:
                input_type = input_item.get("type", "text")
                content = input_item.get("content", input_item)
                
                app_logger.info(f"\n>>> Processing Input {i} (type: {input_type})...")
                result = await orchestrator.process_input(content, input_type)
                
                if result.get("success"):
                    app_logger.info(f"✅ Success: {result.get('title')} [Source: {result.get('source')}]")
                else:
                    app_logger.error(f"❌ Failed: {result.get('error')}")
                    
            except Exception as e:
                app_logger.error(f"❌ Error processing input {i}: {e}")
        
        # Print memory summary
        app_logger.info("\\n" + "=" * 60)
        app_logger.info("Session Summary")
        app_logger.info("=" * 60)
        memory = orchestrator.get_memory_context()
        app_logger.info(f"Total interactions: {len(memory.get('interactions', []))}")
        app_logger.info(f"Tasks created: {len(memory.get('created_tasks', []))}")
        app_logger.info(f"User patterns: {memory.get('patterns', {})}")
        
        await orchestrator.cleanup()
        
        app_logger.info("\\n✅ All tasks completed successfully!")
        
        return 0
    
    except KeyboardInterrupt:
        app_logger.warning("\\nInterrupted by user")
        return 1
    
    except Exception as e:
        app_logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
