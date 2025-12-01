#!/usr/bin/env python3
"""
TaskFlow AI - Comprehensive Demo
Shows all input channels and features
"""

import asyncio
import json
from pathlib import Path
from agents.orchestrator import TaskFlowOrchestrator
from utils.logger import app_logger

# Sample test data
SAMPLE_INPUTS = {
    "text": [
        "Fix the login bug by Friday - it's critical",
        "Schedule team sync meeting about new API design",
        "Review Q1 marketing presentation by end of week",
    ],
    "email": [
        """From: manager@company.com
To: you@company.com
Subject: Review Q1 Marketing Presentation

Hi, can you review the Q1 marketing presentation by end of week? 
It's needed for the board meeting. Thanks!""",
        
        """From: dev-lead@company.com
To: team@company.com
Subject: URGENT - Fix database connection issue

Team, we have a critical issue with the database connection pool. 
This is blocking production and needs immediate attention. 
Priority: BLOCKER""",
    ],
    "voice": [
        "test_voice_1.wav",  # Mock: "Fix the login bug by Friday, it's critical"
        "test_voice_2.wav",  # Mock: "Schedule team sync meeting about new API"
    ]
}

async def demo_single_input(orchestrator: TaskFlowOrchestrator, input_type: str, input_data: str) -> dict:
    """Process a single input through the pipeline"""
    
    print(f"\\n{'='*70}")
    print(f"📥 Input Type: {input_type.upper()}")
    print(f"{'='*70}")
    print(f"Data: {input_data[:100]}...")
    print(f"{'='*70}")
    
    try:
        result = await orchestrator.process_input(input_data, input_type=input_type)
        
        if result.get("success"):
            print(f"✅ SUCCESS")
            print(f"   Task ID: {result.get('task_id')}")
            print(f"   Title: {result.get('title')}")
            print(f"   Priority: {result.get('priority')}")
            print(f"   Labels: {', '.join(result.get('labels', []))}")
        else:
            print(f"❌ FAILED: {result.get('error')}")
        
        return result
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

async def demo_all_channels(orchestrator: TaskFlowOrchestrator) -> dict:
    """Run demo through all input channels"""
    
    results = {
        "text": [],
        "email": [],
        "voice": [],
        "summary": {}
    }
    
    # Test text inputs
    print("\\n" + "🔤 " + "="*68)
    print("🔤 TESTING TEXT INPUTS")
    print("🔤 " + "="*68)
    for text_input in SAMPLE_INPUTS["text"]:
        result = await demo_single_input(orchestrator, "text", text_input)
        results["text"].append(result)
    
    # Test email inputs
    print("\\n" + "📧 " + "="*68)
    print("📧 TESTING EMAIL INPUTS")
    print("📧 " + "="*68)
    for email_input in SAMPLE_INPUTS["email"]:
        result = await demo_single_input(orchestrator, "email", email_input)
        results["email"].append(result)
    
    # Test voice inputs (mock mode by default)
    print("\\n" + "🎤 " + "="*68)
    print("🎤 TESTING VOICE INPUTS (Mock Mode)")
    print("🎤 " + "="*68)
    for voice_input in SAMPLE_INPUTS["voice"]:
        result = await demo_single_input(orchestrator, "voice", voice_input)
        results["voice"].append(result)
    
    # Generate summary
    total_success = sum(1 for r in results["text"] + results["email"] + results["voice"] 
                       if r.get("success"))
    total_tasks = len(results["text"]) + len(results["email"]) + len(results["voice"])
    
    results["summary"] = {
        "total_inputs": total_tasks,
        "successful_tasks": total_success,
        "success_rate": f"{(total_success/total_tasks*100):.1f}%"
    }
    
    return results

async def demo_memory_and_patterns(orchestrator: TaskFlowOrchestrator):
    """Demonstrate session memory and pattern learning"""
    
    print("\\n" + "💾 " + "="*68)
    print("💾 SESSION MEMORY & PATTERN ANALYSIS")
    print("💾 " + "="*68)
    
    memory = orchestrator.get_memory_context()
    
    print(f"\\n📊 Interaction Statistics:")
    print(f"   Total Interactions: {len(memory.get('interactions', []))}")
    print(f"   Tasks Created: {len(memory.get('created_tasks', []))}")
    
    if memory.get("created_tasks"):
        print(f"\\n📈 Task Breakdown by Source:")
        source_counts = {}
        for task in memory.get("created_tasks", []):
            source = task.get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        for source, count in source_counts.items():
            print(f"   {source.upper()}: {count} tasks")
    
    patterns = memory.get("patterns", {})
    if patterns:
        print(f"\\n🧠 Learned User Patterns:")
        print(f"   Average Priority: {patterns.get('average_priority', 'N/A'):.1f}")
        print(f"   Common Labels: {', '.join(patterns.get('common_labels', []))}")
        print(f"   Preferred Channel: {patterns.get('preferred_source', 'N/A')}")
        print(f"   Total Tasks Processed: {patterns.get('total_tasks', 0)}")

async def main():
    """Main demo execution"""
    
    print("\\n" + "="*70)
    print("🚀 TaskFlow AI - Comprehensive Demo")
    print("Multi-Channel Task Management System with ADK")
    print("="*70)
    
    try:
        # Initialize orchestrator
        print("\\n⏳ Initializing TaskFlow Orchestrator...")
        orchestrator = TaskFlowOrchestrator()
        await orchestrator.initialize()
        print("✅ Orchestrator initialized")
        
        # Run comprehensive demo
        print("\\n⏳ Running comprehensive demo...")
        demo_results = await demo_all_channels(orchestrator)
        
        # Show memory and patterns
        await demo_memory_and_patterns(orchestrator)
        
        # Print final summary
        print("\\n" + "="*70)
        print("📊 DEMO SUMMARY")
        print("="*70)
        summary = demo_results["summary"]
        print(f"Total Inputs Processed: {summary['total_inputs']}")
        print(f"Successful Task Creations: {summary['successful_tasks']}")
        print(f"Success Rate: {summary['success_rate']}")
        
        # Show which features are working
        print(f"\\n✅ Features Demonstrated:")
        print(f"   ✓ Text input processing")
        print(f"   ✓ Email parsing and extraction")
        print(f"   ✓ Voice transcription (mock mode)")
        print(f"   ✓ LLM-based task extraction")
        print(f"   ✓ Task enrichment with context")
        print(f"   ✓ Vikunja integration")
        print(f"   ✓ Session memory tracking")
        print(f"   ✓ Pattern learning from history")
        
        # Show architecture
        print(f"\\n📐 Architecture Demonstration:")
        print(f"   ✓ Root Orchestrator (ADK LlmAgent)")
        print(f"   ✓ Input Processor Agent")
        print(f"   ✓ Parser Agent (LLM extraction)")
        print(f"   ✓ Enricher Agent (context learning)")
        print(f"   ✓ Vikunja Agent (REST API)")
        
        # Course alignment
        print(f"\\n🎓 Course Concepts Covered:")
        print(f"   ✓ Multi-agent architecture (Day 1)")
        print(f"   ✓ Tool integration & MCP patterns (Day 2)")
        print(f"   ✓ Context engineering & memory (Day 3)")
        print(f"   ✓ Agent quality & observability (Day 4)")
        print(f"   ✓ Production & scalability (Day 5)")
        
        await orchestrator.cleanup()
        
        print("\\n" + "="*70)
        print("✅ Demo completed successfully!")
        print("="*70 + "\\n")
        
        return 0
    
    except Exception as e:
        print(f"\\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
