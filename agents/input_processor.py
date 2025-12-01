"""Input Processing Agent - Normalizes voice, email, text to natural language"""

from typing import Dict, Any, Tuple
from utils.logger import app_logger
from tools.email_tools import email_processor
from tools.voice_tools import voice_processor

class InputProcessorAgent:
    """Processes multi-channel input"""
    
    def detect_input_type(self, text: str) -> str:
        """Auto-detect input type from content"""
        
        text_lower = str(text).lower()
        
        # Check for email headers (From:, To:, Subject:)
        email_indicators = [
            text_lower.startswith("from:"),
            "to:" in text_lower,
            "subject:" in text_lower,
        ]
        
        if any(email_indicators):
            app_logger.info("Auto-detected: EMAIL format")
            return "email"
        
        # Check for voice indicators
        voice_indicators = [
            "[voice]" in text_lower,
            "audio:" in text_lower,
            ".wav" in text_lower or ".mp3" in text_lower,
        ]
        
        if any(voice_indicators):
            app_logger.info("Auto-detected: VOICE format")
            return "voice"
        
        # Default to text
        app_logger.info("Auto-detected: TEXT format")
        return "text"
    
    async def process_text(self, text: str) -> Tuple[str, str]:
        """Process direct text input"""
        normalized = text.strip()
        app_logger.info(f"Text input processed: {len(normalized)} chars")
        return normalized, "text"
    
    async def process_email(self, email_text: str) -> Tuple[str, str]:
        """Process email input"""
        email_data = email_processor.parse_email(email_text)
        actionable_text = email_processor.extract_actionable_text(email_data)
        app_logger.info(f"Email processed from {email_data['from']}")
        return actionable_text, "email"
    
    async def process_voice(self, audio_path: str) -> Tuple[str, str]:
        """Process voice input"""
        transcribed = voice_processor.transcribe(audio_path)
        app_logger.info(f"Voice transcribed: {len(transcribed)} chars")
        return transcribed, "voice"
    
    async def detect_and_process(self, input_data: Any, input_type: str = "text") -> Tuple[str, str]:
        """Auto-detect and process input - IMPROVED VERSION"""
        
        # Convert input_data to string to analyze
        text_content = str(input_data) if not isinstance(input_data, str) else input_data
        
        # IMPROVEMENT: Auto-detect type from content FIRST
        detected_type = self.detect_input_type(text_content)
        
        # Use detected type unless explicitly overridden with "text"
        # (keep explicit type parameter as fallback)
        if input_type != "text" and input_type in ["email", "voice"]:
            detected_type = input_type
        
        app_logger.info(f"Processing as: {detected_type}")
        
        # Process based on DETECTED type
        if detected_type == "email":
            return await self.process_email(text_content)
        elif detected_type == "voice":
            return await self.process_voice(text_content)
        else:
            return await self.process_text(text_content)

input_processor_agent = InputProcessorAgent()
