import os
import httpx
import asyncio
import json
from typing import Dict, Any, Optional

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.session = httpx.AsyncClient(timeout=60.0)
    
    async def call_openrouter_api(self, prompt: str, model: str = "deepseek/deepseek-chat-v3.1:free", task_type: str = "general") -> str:
        """Call OpenRouter API with specified model and prompt"""
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://luna-ai.com",
            "X-Title": "Luna AI Enterprise"
        }
        
        # Model selection based on task type
        model_mapping = {
            "general": "deepseek/deepseek-chat-v3.1:free",
            "analysis": "moonshotai/kimi-k2-0905", 
            "research": "microsoft/phi-4",
            "classification": "deepseek/deepseek-chat-v3.1:free",
            "synthesis": "moonshotai/kimi-k2-0905",
            "strategy": "moonshotai/kimi-k2-0905",
            "planning": "deepseek/deepseek-chat-v3.1:free"
        }
        
        selected_model = model_mapping.get(task_type, model)
        
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        try:
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    async def close(self):
        """Close the HTTP session"""
        await self.session.aclose()
