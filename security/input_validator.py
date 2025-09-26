"""
Input validation and sanitization for Luna AI
Prevent prompt injection and malicious inputs
"""
import re
from typing import Dict, Any, List, Optional, Union
from fastapi import HTTPException
import html
import logging


class LunaInputValidator:
    """Comprehensive input validation and sanitization"""

    def __init__(self):
        # Dangerous patterns that could indicate prompt injection
        self.prompt_injection_patterns = [
            r'ignore\s+previous\s+instructions',
            r'forget\s+everything',
            r'new\s+instructions',
            r'system\s*:\s*',
            r'assistant\s*:\s*',
            r'human\s*:\s*',
            r'<\s*instruction\s*>',
            r'</\s*instruction\s*>',
            r'$$\s*system\s*$$',
            r'$$\s*/\s*system\s*$$',
            r'override\s+your\s+programming',
            r'act\s+as\s+(?:if|though)',
            r'pretend\s+(?:to\s+be|you\s+are)',
            r'roleplay\s+as',
            r'simulate\s+being',
        ]

        # SQL injection patterns
        self.sql_injection_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC)\b)',
            r'(\b(UNION|JOIN|WHERE|HAVING|ORDER BY|GROUP BY)\b)',
            r'(--|\#|\/\*|\*\/)',
            r'(\bOR\b.*\b=\b|\bAND\b.*\b=\b)',
            r'(\'\s*(OR|AND)\s*\')',
        ]

        # XSS patterns
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',
        ]

        # Maximum lengths
        self.max_lengths = {
            "query": 2000,
            "email": 254,
            "username": 50,
            "niche": 100,
            "instagram_handle": 50
        }

    def validate_query(self, query: str) -> str:
        """Validate and sanitize user query"""
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        query = query.strip()

        # Check length
        if len(query) > self.max_lengths["query"]:
            raise HTTPException(
                status_code=400,
                detail=f"Query too long. Maximum length: {self.max_lengths['query']} characters"
            )

        # Check for prompt injection
        if self._detect_prompt_injection(query):
            logging.warning(f"Prompt injection attempt detected: {query[:100]}...")
            raise HTTPException(
                status_code=400,
                detail="Invalid query format. Please rephrase your question."
            )

        # Check for SQL injection
        if self._detect_sql_injection(query):
            logging.warning(f"SQL injection attempt detected: {query[:100]}...")
            raise HTTPException(
                status_code=400,
                detail="Invalid characters in query. Please use only letters, numbers, and basic punctuation."
            )

        # Check for XSS
        if self._detect_xss(query):
            logging.warning(f"XSS attempt detected: {query[:100]}...")
            raise HTTPException(
                status_code=400,
                detail="Invalid characters in query. HTML and scripts are not allowed."
            )

        # HTML escape for safety
        query = html.escape(query, quote=False)

        return query

    def validate_email(self, email: str) -> str:
        """Validate email format"""
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")

        email = email.strip().lower()

        if len(email) > self.max_lengths["email"]:
            raise HTTPException(status_code=400, detail="Email address too long")

        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        return email

    def validate_instagram_handle(self, handle: str) -> str:
        """Validate Instagram handle"""
        if not handle:
            return ""

        handle = handle.strip()

        # Remove @ if present
        if handle.startswith('@'):
            handle = handle[1:]

        if len(handle) > self.max_lengths["instagram_handle"]:
            raise HTTPException(status_code=400, detail="Instagram handle too long")

        # Instagram handle pattern
        instagram_pattern = r'^[a-zA-Z0-9._]{1,30}$'
        if not re.match(instagram_pattern, handle):
            raise HTTPException(
                status_code=400,
                detail="Invalid Instagram handle. Use only letters, numbers, dots, and underscores."
            )

        return handle

    def validate_niche(self, niche: str) -> str:
        """Validate niche/category"""
        if not niche:
            return ""

        niche = niche.strip()

        if len(niche) > self.max_lengths["niche"]:
            raise HTTPException(status_code=400, detail="Niche description too long")

        # Only allow letters, numbers, spaces, and basic punctuation
        niche_pattern = r'^[a-zA-Z0-9\s\-_&,\.]+$'
        if not re.match(niche_pattern, niche):
            raise HTTPException(
                status_code=400,
                detail="Invalid characters in niche. Use only letters, numbers, and basic punctuation."
            )

        return niche.lower()

    def validate_account_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize account context"""
        validated_context = {}

        # Validate follower count
        if "followers" in context:
            followers = context["followers"]
            if isinstance(followers, (int, float)) and followers >= 0:
                validated_context["followers"] = int(followers)
            elif isinstance(followers, str) and followers.isdigit():
                validated_context["followers"] = int(followers)

        # Validate engagement rate
        if "engagement_rate" in context:
            engagement_rate = context["engagement_rate"]
            if isinstance(engagement_rate, (int, float)) and 0 <= engagement_rate <= 1:
                validated_context["engagement_rate"] = float(engagement_rate)

        # Validate niche
        if "niche" in context and context["niche"]:
            validated_context["niche"] = self.validate_niche(context["niche"])

        # Validate business type
        if "business_type" in context:
            business_type = context["business_type"]
            valid_types = ["personal", "business", "creator"]
            if business_type in valid_types:
                validated_context["business_type"] = business_type

        # Validate posting frequency
        if "posting_frequency" in context:
            posting_freq = context["posting_frequency"]
            if isinstance(posting_freq, (int, float)) and posting_freq >= 0:
                validated_context["posting_frequency"] = int(posting_freq)

        return validated_context

    def _detect_prompt_injection(self, text: str) -> bool:
        """Detect potential prompt injection attempts"""
        text_lower = text.lower()

        for pattern in self.prompt_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        return False

    def _detect_sql_injection(self, text: str) -> bool:
        """Detect potential SQL injection attempts"""
        text_upper = text.upper()

        for pattern in self.sql_injection_patterns:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True

        return False

    def _detect_xss(self, text: str) -> bool:
        """Detect potential XSS attempts"""
        text_lower = text.lower()

        for pattern in self.xss_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        return False


# Global input validator instance
input_validator = LunaInputValidator()
