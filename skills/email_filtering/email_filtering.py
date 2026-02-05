"""
Email Filtering Skill
Provides keyword filtering and email categorization
"""
from typing import List, Dict, Any

class EmailFilteringSkill:
    """Filter and categorize emails based on keywords"""
    
    def __init__(self, keywords: List[str]):
        self.keywords = [k.lower().strip() for k in keywords]
    
    def is_relevant(self, subject: str, body: str = "") -> bool:
        """Check if email contains any filter keywords"""
        text = f"{subject} {body}".lower()
        return any(keyword in text for keyword in self.keywords)
    
    def extract_keywords(self, subject: str, body: str = "") -> List[str]:
        """Extract matching keywords from email"""
        text = f"{subject} {body}".lower()
        return [kw for kw in self.keywords if kw in text]
    
    def detect_quiz_alert(self, subject: str, body: str = "") -> bool:
        """Detect if email is about a quiz or exam"""
        quiz_keywords = ["quiz", "exam", "test", "assessment"]
        text = f"{subject} {body}".lower()
        return any(keyword in text for keyword in quiz_keywords)
    
    def detect_deadline(self, subject: str, body: str = "") -> bool:
        """Detect if email mentions a deadline"""
        deadline_keywords = ["deadline", "due date", "submit by", "submission"]
        text = f"{subject} {body}".lower()
        return any(keyword in text for keyword in deadline_keywords)
    
    def categorize_email(self, subject: str, body: str = "") -> Dict[str, Any]:
        """Categorize email and extract metadata"""
        return {
            "is_relevant": self.is_relevant(subject, body),
            "keywords": self.extract_keywords(subject, body),
            "is_quiz": self.detect_quiz_alert(subject, body),
            "has_deadline": self.detect_deadline(subject, body),
            "priority": self._calculate_priority(subject, body)
        }
    
    def _calculate_priority(self, subject: str, body: str = "") -> str:
        """Calculate email priority"""
        text = f"{subject} {body}".lower()
        
        high_priority = ["urgent", "quiz", "exam", "deadline", "today", "tomorrow"]
        if any(keyword in text for keyword in high_priority):
            return "high"
        
        medium_priority = ["assignment", "submission", "meeting"]
        if any(keyword in text for keyword in medium_priority):
            return "medium"
        
        return "low"
