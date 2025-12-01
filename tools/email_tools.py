from typing import Dict, Any
import re
from utils.logger import app_logger

class EmailProcessor:
    """Parse email content"""
    
    @staticmethod
    def parse_email(email_text: str) -> Dict[str, str]:
        """Extract email components"""
        
        result = {
            "from": "",
            "to": "",
            "subject": "",
            "body": ""
        }
        
        lines = email_text.split("\n")
        body_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith("From:"):
                result["from"] = line.replace("From:", "").strip()
            elif line.startswith("To:"):
                result["to"] = line.replace("To:", "").strip()
            elif line.startswith("Subject:"):
                result["subject"] = line.replace("Subject:", "").strip()
            elif line.strip() == "":
                body_start = i + 1
                break
        
        result["body"] = "\n".join(lines[body_start:]).strip()
        
        return result
    
    @staticmethod
    def extract_actionable_text(email_data: Dict[str, str]) -> str:
        """Convert email to actionable text for task extraction"""
        
        # Combine subject + body
        text = f"{email_data['subject']}. {email_data['body']}"
        
        # Remove common email signatures
        text = re.sub(r"^\s*--.*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*Best,.*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*Thanks,.*", "", text, flags=re.MULTILINE)
        
        return text.strip()

email_processor = EmailProcessor()
