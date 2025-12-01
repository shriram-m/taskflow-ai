import os
from typing import Optional
from pathlib import Path
from utils.logger import app_logger

class VoiceProcessor:
    """Handle voice input - Real or Mock mode"""
    
    def __init__(self, mode: str = "mock", service: str = "whisper"):
        """
        mode: "real" for API calls, "mock" for testing
        service: "whisper" or "gemini_audio"
        """
        self.mode = mode
        self.service = service
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self) -> dict:
        """Load mock transcriptions for testing"""
        return {
            "test_voice_1.wav": "Fix the login bug by Friday, it's critical",
            "test_voice_2.wav": "Schedule team sync meeting about new API",
            "test_voice_3.wav": "Review Q1 presentation, needs feedback",
        }
    
    def transcribe(self, file_path: str) -> str:
        """Transcribe audio file"""
        
        if self.mode == "mock":
            return self._transcribe_mock(file_path)
        else:
            return self._transcribe_real(file_path)
    
    def _transcribe_mock(self, file_path: str) -> str:
        """Mock transcription for testing"""
        file_name = Path(file_path).name
        
        if file_name in self.mock_data:
            text = self.mock_data[file_name]
            app_logger.info(f"Mock transcription: {file_name} → {text}")
            return text
        else:
            # Fallback mock response
            app_logger.warning(f"No mock data for {file_name}, returning generic response")
            return "Create new task with urgency"
    
    def _transcribe_real(self, file_path: str) -> str:
        """Real transcription using API"""
        
        # Verify file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        if self.service == "whisper":
            return self._transcribe_with_whisper(file_path)
        elif self.service == "gemini_audio":
            return self._transcribe_with_gemini_audio(file_path)
        else:
            raise ValueError(f"Unknown voice service: {self.service}")
    
    def _transcribe_with_whisper(self, file_path: str) -> str:
        """Transcribe using Whisper API"""
        try:
            import openai
            
            api_key = os.getenv("WHISPER_API_KEY")
            if not api_key:
                raise ValueError("WHISPER_API_KEY not set")
            
            client = openai.OpenAI(api_key=api_key)
            
            with open(file_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                )
            
            app_logger.info(f"Whisper transcription: {transcript.text}")
            return transcript.text
        
        except Exception as e:
            app_logger.error(f"Whisper error: {e}")
            raise
    
    def _transcribe_with_gemini_audio(self, file_path: str) -> str:
        """Transcribe using Gemini Audio API"""
        try:
            from tools.gemini_tools import gemini_service
            return gemini_service.transcribe_audio_with_gemini(file_path)
        except Exception as e:
            app_logger.error(f"Gemini audio error: {e}")
            raise

voice_processor = VoiceProcessor(
    mode=os.getenv("VOICE_MODE", "mock"),
    service=os.getenv("VOICE_SERVICE", "whisper")
)
