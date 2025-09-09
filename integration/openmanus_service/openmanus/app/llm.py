import logging
import time

logger = logging.getLogger("luna.llm")

import os
import requests
from typing import Dict, List, Optional
import re

class LLM:
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.embed_model = os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_host}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def is_available(self) -> bool:
        return self.available
    
    def understand_text(self, text: str) -> Dict:
    """Process Instagram growth goals with semantic understanding"""
    # Start timing and log the processing start
    start_time = time.perf_counter()
    logger.info("🧠 Luna LLM PROCESSING: %s", text[:50] + "..." if len(text) > 50 else text)
    
    try:
        # Your existing logic - no changes needed here
        result = {
            "understood": True,
            "text": text,
            "analysis": self._analyze_instagram_goal(text)
        }
        
        # Log successful completion with timing
        duration = time.perf_counter() - start_time
        logger.info("🧠 Luna LLM COMPLETED: %.3fs", duration)
        
        return result
        
    except Exception as e:
        # Log error with timing
        duration = time.perf_counter() - start_time
        logger.exception("🧠 Luna LLM ERROR after %.3fs: %s", duration, str(e))
        
        return {"understood": False, "error": str(e)}

        
        # Extract follower numbers
        followers_match = re.search(r'(\d+)\s*(?:to\s*)?(\d+)\s*followers?', text_lower)
        if followers_match:
            analysis["current_followers"] = int(followers_match.group(1))
            analysis["target_followers"] = int(followers_match.group(2))
            growth = int(followers_match.group(2)) - int(followers_match.group(1))
            analysis["growth_target"] = growth
            analysis["growth_percentage"] = f"{(growth / int(followers_match.group(1))) * 100:.0f}%"
        
        # Extract timeframe
        time_match = re.search(r'(\d+)\s*(days?|weeks?|months?)', text_lower)
        if time_match:
            analysis["timeframe"] = f"{time_match.group(1)} {time_match.group(2)}"
            analysis["timeframe_days"] = self._convert_to_days(time_match.group(1), time_match.group(2))
        
        # Extract niche/vertical
        niches = ["fitness", "fashion", "food", "travel", "business", "lifestyle", "beauty", "tech", "music"]
        for niche in niches:
            if niche in text_lower:
                analysis["niche"] = niche
                analysis["industry"] = niche
                break
                
        return analysis
    
    def _convert_to_days(self, number: str, unit: str) -> int:
        """Convert time units to days"""
        days = int(number)
        if "week" in unit:
            days *= 7
        elif "month" in unit:
            days *= 30
        return days
