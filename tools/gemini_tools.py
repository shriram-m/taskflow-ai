import json
from typing import Dict, Any, Optional
import google.genai as genai
from utils.logger import app_logger

# Import settings from config (this loads .env automatically)
from config import settings

class GeminiLLMService:
    """Wrapper around Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use settings object instead of os.getenv()
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            app_logger.warning("GEMINI_API_KEY not set in config/environment")
        self.model = "gemini-2.5-flash"
    
    def extract_task_structure(self, text: str) -> Dict[str, Any]:
        """Extract structured task from natural language"""
        
        if not self.api_key:
            app_logger.error("Cannot call Gemini API without API key")
            return {
                "title": text[:50],
                "description": text,
                "priority": 1,
                "due_date": None,
                "labels": ["inbox"]
            }
        
        prompt = f"""Extract task information from this text:
        
Text: {text}

Return ONLY a JSON object (no markdown, no extra text) with these fields:
- title: Brief task title
- description: More detailed description
- priority: 0 (low) to 3 (urgent)
- due_date: YYYY-MM-DD or null
- labels: List of relevant tags

Example:
{{"title": "Fix login bug", "description": "Auth page broken", "priority": 2, "due_date": "2025-12-05", "labels": ["bug", "auth"]}}

Response:"""
        
        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=500
                )
            )
            
            # FIX: Check if response.text is None
            if not response or not response.text:
                app_logger.warning("Gemini returned empty response")
                return {
                    "title": text[:50],
                    "description": text,
                    "priority": 1,
                    "due_date": None,
                    "labels": ["inbox"]
                }
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            task_data = json.loads(response_text.strip())
            
            # Validate required fields
            assert "title" in task_data, "Missing title"
            assert isinstance(task_data.get("priority", 0), int), "Priority must be int"
            
            return task_data
            
        except Exception as e:
            app_logger.error(f"Error extracting task: {e}")
            return {
                "title": text[:50],
                "description": text,
                "priority": 1,
                "due_date": None,
                "labels": ["inbox"]
            }
    
    def enrich_task(self, task: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        """Enhance task with context and patterns"""
        
        if not self.api_key:
            app_logger.warning("Cannot enrich task without API key, returning original")
            return task
        
        prompt = f"""Improve this task using the provided context:

Task:
{json.dumps(task, indent=2)}

Context:
{context}

Rules:
1. If task seems urgent (keywords: critical, blocker, ASAP), increase priority
2. Suggest relevant labels based on the task
3. Fill missing due_date if context suggests timing
4. Keep title concise

Return ONLY JSON with the same structure, enhanced fields:"""
        
        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=500
                )
            )
            
            # FIX: Check if response.text is None
            if not response or not response.text:
                app_logger.warning("Gemini returned empty response for enrichment")
                return task
            
            response_text = response.text.strip()
            
            # Clean markdown if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            enriched = json.loads(response_text.strip())

            # Merge with original
            result = {**task, **enriched}
            return result
            
        except Exception as e:
            app_logger.warning(f"Error enriching task: {e}, returning original")
            return task

    def transcribe_audio_with_gemini(self, file_path: str) -> str:
        """Transcribe audio using Gemini Audio API"""
        
        if not self.api_key:
            raise ValueError("Cannot transcribe without API key")
        
        try:
            client = genai.Client(api_key=self.api_key)
            
            with open(file_path, "rb") as f:
                audio_data = f.read()
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "Transcribe this audio and return ONLY the transcribed text, nothing else:",
                    {
                        "mime_type": "audio/wav",
                        "data": audio_data
                    }
                ]
            )
            
            return response.text.strip()
        
        except Exception as e:
            app_logger.error(f"Error transcribing audio: {e}")
            raise

# Create singleton instance
try:
    gemini_service = GeminiLLMService()
    app_logger.info("Gemini service initialized with API key")
except Exception as e:
    app_logger.warning(f"Could not initialize Gemini service: {e}")
    gemini_service = None
