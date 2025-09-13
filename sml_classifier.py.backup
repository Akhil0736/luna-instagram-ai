import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
import time
from typing import Dict, List, Tuple
from functools import lru_cache
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LunaQueryClassifier:
    """
    Lightweight SML-based query classifier for intelligent routing
    Uses DistilBERT for fast, accurate query classification
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classification_cache = {}
        self.load_model()
    
    def load_model(self):
        """Load the SML classification model"""
        try:
            logger.info(f"🤖 Loading SML classifier: {self.model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"✅ SML classifier loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"❌ Failed to load SML classifier: {e}")
            raise
    
    @lru_cache(maxsize=1000)
    def classify_query_intent(self, query: str) -> str:
        """
        Classify query intent using SML + rule-based logic
        Returns: simple_chat, instagram_research, competitor_analysis, coding, general
        """
        start_time = time.perf_counter()
        
        # Normalize query
        query_lower = query.strip().lower()
        
        # Fast rule-based classification first (ultra-fast path)
        if len(query) < 10:
            return "simple_chat"
        
        # Rule-based patterns (0.0001 seconds)
        simple_patterns = ["hi", "hello", "thanks", "thank you", "bye", "goodbye"]
        if any(pattern in query_lower for pattern in simple_patterns):
            return "simple_chat"
        
        research_patterns = ["algorithm", "trend", "latest", "research", "study", "data", "analytics"]
        if any(pattern in query_lower for pattern in research_patterns):
            return "instagram_research"
        
        competitor_patterns = ["competitor", "analyze", "compare", "versus", "vs", "competitive"]
        if any(pattern in query_lower for pattern in competitor_patterns):
            return "competitor_analysis"
        
        coding_patterns = ["code", "script", "automation", "bot", "api", "program", "function"]
        if any(pattern in query_lower for pattern in coding_patterns):
            return "coding"
        
        # Instagram-specific patterns
        instagram_patterns = ["instagram", "insta", "reel", "story", "hashtag", "follower", "engagement"]
        if any(pattern in query_lower for pattern in instagram_patterns):
            return "instagram_research"
        
        # SML classification for complex queries (0.01-0.1 seconds)
        try:
            sml_result = self._sml_classify(query)
            classification_time = time.perf_counter() - start_time
            
            logger.info(f"🧠 SML classified '{query[:30]}...' → {sml_result} ({classification_time:.3f}s)")
            return sml_result
            
        except Exception as e:
            logger.warning(f"⚠️ SML classification failed, using fallback: {e}")
            return "general"
    
    def _sml_classify(self, query: str) -> str:
        """Internal SML classification using DistilBERT"""
        # Tokenize input
        inputs = self.tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=-1)
            predicted_class_id = logits.argmax().item()
            confidence = probabilities.max().item()
        
        # Map sentiment to Luna query types (customize based on your needs)
        if confidence < 0.7:
            return "general"  # Low confidence = general handling
        
        # Map DistilBERT sentiment to Luna categories
        # POSITIVE sentiment -> likely actionable/research queries
        # NEGATIVE sentiment -> likely support/troubleshooting queries
        sentiment_label = self.model.config.id2label[predicted_class_id]
        
        if sentiment_label == "POSITIVE":
            return "instagram_research"  # Positive queries are often growth-focused
        else:
            return "general"  # Negative or neutral queries get general handling
    
    def get_model_recommendation(self, query_type: str) -> Tuple[str, int]:
        """
        Recommend LLM model and TTL based on classification
        Returns: (model_name, cache_ttl_seconds)
        """
        model_recommendations = {
            "simple_chat": ("microsoft/phi-3-mini-4k-instruct", 86400),      # 24 hours
            "instagram_research": ("moonshot/kimi-k2", 600),                  # 10 minutes
            "competitor_analysis": ("moonshot/kimi-k2", 1800),                # 30 minutes
            "coding": ("deepseek/deepseek-r1", 43200),                       # 12 hours
            "general": ("moonshot/kimi", 3600)                               # 1 hour
        }
        
        return model_recommendations.get(query_type, ("moonshot/kimi", 3600))
    
    def analyze_query_complexity(self, query: str) -> Dict[str, any]:
        """
        Analyze query complexity for advanced routing
        """
        return {
            "length": len(query),
            "word_count": len(query.split()),
            "has_questions": "?" in query,
            "has_technical_terms": any(term in query.lower() for term in 
                                     ["api", "algorithm", "code", "technical", "implementation"]),
            "estimated_response_time": 0.05 if len(query) < 50 else 0.1
        }
    
    def get_classification_stats(self) -> Dict[str, any]:
        """Get classification performance statistics"""
        return {
            "cache_size": len(self.classification_cache),
            "model_device": str(self.device),
            "model_loaded": self.model is not None
        }

# Global SML classifier instance
luna_classifier = LunaQueryClassifier()
