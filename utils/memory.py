from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json

@dataclass
class Interaction:
    """Represents a user interaction"""
    type: str  # "voice", "email", "text"
    content: str
    timestamp: str
    channel: str
    task_created: bool = False

@dataclass
class TaskMemory:
    """Represents a created task in memory"""
    task_id: int
    title: str
    source: str  # "voice", "email", "text"
    created_at: str
    priority: int
    labels: List[str]

class SessionMemory:
    """In-memory session storage with TTL"""
    
    def __init__(self, ttl_seconds: int = 3600, max_items: int = 100):
        self.interactions: List[Interaction] = []
        self.created_tasks: List[TaskMemory] = []
        self.ttl = ttl_seconds
        self.max_items = max_items
    
    def add_interaction(self, type_: str, content: str, channel: str) -> None:
        """Add user interaction to memory"""
        interaction = Interaction(
            type=type_,
            content=content,
            timestamp=datetime.utcnow().isoformat(),
            channel=channel
        )
        self.interactions.append(interaction)
        
        # Keep only recent items
        if len(self.interactions) > self.max_items:
            self.interactions = self.interactions[-self.max_items:]
    
    def add_task_created(self, task_id: int, title: str, source: str, 
                        priority: int, labels: List[str]) -> None:
        """Track created task"""
        task = TaskMemory(
            task_id=task_id,
            title=title,
            source=source,
            created_at=datetime.utcnow().isoformat(),
            priority=priority,
            labels=labels
        )
        self.created_tasks.append(task)
        
        if len(self.created_tasks) > self.max_items:
            self.created_tasks = self.created_tasks[-self.max_items:]
    
    def get_context(self, limit: int = 5) -> str:
        """Get recent context for enrichment"""
        recent_tasks = self.created_tasks[-limit:]
        context = "Recent tasks created:\n"
        for task in recent_tasks:
            context += f"- {task.title} (Priority: {task.priority}, Labels: {', '.join(task.labels)})\n"
        return context
    
    def get_user_patterns(self) -> Dict[str, Any]:
        """Extract user patterns from history"""
        if not self.created_tasks:
            return {}
        
        # Analyze patterns
        avg_priority = sum(t.priority for t in self.created_tasks) / len(self.created_tasks)
        all_labels = set()
        for task in self.created_tasks:
            all_labels.update(task.labels)
        
        sources = {}
        for task in self.created_tasks:
            sources[task.source] = sources.get(task.source, 0) + 1
        
        return {
            "average_priority": avg_priority,
            "common_labels": list(all_labels),
            "preferred_source": max(sources, key=sources.get) if sources else None,
            "total_tasks": len(self.created_tasks)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            "interactions": [asdict(i) for i in self.interactions],
            "created_tasks": [asdict(t) for t in self.created_tasks],
            "patterns": self.get_user_patterns()
        }
