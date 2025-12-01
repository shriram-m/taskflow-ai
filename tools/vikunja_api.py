import requests
from typing import Dict, Any, Optional
from datetime import datetime
from utils.logger import app_logger
from config import settings

# Color coding by input source
COLOR_MAPPING = {
    "voice": "#03346E",      # Dark Blue (voice input)
    "email": "#8C3061",      # Plum (email input)
    "text": "#1A3636",       # Dark Teal (text input)
    "default": "#000000"     # Black (fallback)
}

class VikunjaBClient:
    """Vikunja REST API client - Fixed version"""
    
    def __init__(self, url: str = None, username: str = None, password: str = None, project_id: int = None):
        self.base_url = (url or settings.VIKUNJA_URL).rstrip("/")
        self.username = username or settings.VIKUNJA_USERNAME
        self.password = password or settings.VIKUNJA_PASSWORD
        self.project_id = project_id or settings.VIKUNJA_PROJECT_ID
        self.token: Optional[str] = None
        self.headers = {"Content-Type": "application/json"}
    
    def authenticate(self) -> bool:
        """Login to Vikunja"""
        try:
            url = f"{self.base_url}/api/v1/login"
            payload = {"username": self.username, "password": self.password}
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                self.token = response.json().get("token")
                self.headers["Authorization"] = f"Bearer {self.token}"
                app_logger.info("Vikunja authentication successful")
                return True
            else:
                app_logger.error(f"Auth failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            app_logger.error(f"Authentication error: {e}")
            return False
    
    def create_task(self, title: str, description: str, priority: int, 
                   due_date: Optional[str], labels: list, source_type: str = "text") -> Dict[str, Any]:
        """Create task in Vikunja with color based on source (voice/email/text)"""
        
        if not self.token:
            if not self.authenticate():
                raise Exception("Not authenticated with Vikunja")
        
        # Map source type to color
        hex_color = COLOR_MAPPING.get(source_type.lower(), COLOR_MAPPING["default"])
        
        # Format date properly
        if due_date:
            try:
                # Parse if it's a date string
                dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                start_date = dt.strftime("%Y-%m-%dT00:00:00Z")
            except:
                start_date = due_date
        else:
            start_date = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
        
        # Build payload - CRITICAL: Use PUT not POST!
        payload = {
            "title": title,
            "project_id": self.project_id,  # ← REQUIRED!
            "start_date": start_date,       # ← REQUIRED!
            "hex_color": hex_color,         # ← FOR COLORS!
        }
        
        # Add optional fields
        if description:
            payload["description"] = description
        if priority is not None:
            payload["priority"] = priority
        
        try:
            response = requests.put(
                f"{self.base_url}/api/v1/projects/{self.project_id}/tasks",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code in [200, 201]:
                task = response.json()
                task_id = task.get("id")
                
                app_logger.info(f"Task created: {task_id} - {title} [Color: {hex_color}, Source: {source_type}]")
                return task
            else:
                app_logger.error(f"Failed to create task: {response.status_code}")
                app_logger.error(f"Response: {response.text}")
                raise Exception(f"Vikunja error: {response.text}")
        
        except Exception as e:
            app_logger.error(f"Error creating task: {e}")
            raise
    
    def list_tasks(self) -> list:
        """List all tasks in project"""
        
        if not self.token:
            if not self.authenticate():
                return []
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/projects/{self.project_id}/tasks",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                app_logger.error(f"Failed to list tasks: {response.status_code}")
                return []
        
        except Exception as e:
            app_logger.error(f"Error listing tasks: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test Vikunja connection"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            app_logger.error(f"Connection test failed: {e}")
            return False

def create_vikunja_client() -> VikunjaBClient:
    """Factory function - uses settings automatically"""
    return VikunjaBClient()
