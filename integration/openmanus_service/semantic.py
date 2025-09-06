from __future__ import annotations

import os
import math
from typing import List, Optional, Tuple, Dict, Any

import asyncio

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None  # type: ignore

# Optional backends
_ollama_available = False
try:  # pragma: no cover - optional
    import ollama  # type: ignore
    _ollama_available = True
except Exception:
    pass

_transformers_available = False
try:  # pragma: no cover - optional
    from transformers import AutoTokenizer, AutoModel
    import torch
    _transformers_available = True
except Exception:
    AutoTokenizer = AutoModel = None  # type: ignore
    torch = None  # type: ignore


class EmbeddingsEngine:
    """
    Pluggable embeddings engine with two backends:
    - Ollama local model (preferred if OLLAMA_HOST set and model present)
    - Transformers (Hugging Face) local model

    By default targets Google's EmbeddingGemma if available. You can override via env:
      EMBEDDING_MODEL=google/embedding-gemma  (Transformers)
      OLLAMA_EMBED_MODEL=embedding-gemma      (Ollama model tag)
    """

    def __init__(self) -> None:
        self.backend: str = os.getenv("EMBEDDINGS_BACKEND", "auto")
        self.model_name: str = os.getenv("EMBEDDING_MODEL", "google/embedding-gemma")
        self.ollama_model: str = os.getenv("OLLAMA_EMBED_MODEL", "embedding-gemma")
        self._tok = None
        self._mdl = None

        # Auto-select backend
        if self.backend == "auto":
            if os.getenv("OLLAMA_HOST") and _ollama_available:
                self.backend = "ollama"
            elif _transformers_available:
                self.backend = "transformers"
            else:
                self.backend = "noop"
        # Initialize lazily for transformers

    def _ensure_transformers(self) -> None:
        if not _transformers_available:
            raise RuntimeError("Transformers backend not available. Install transformers and torch.")
        if self._tok is None or self._mdl is None:
            # For EmbeddingGemma, we assume a sentence embedding interface via mean pooling
            self._tok = AutoTokenizer.from_pretrained(self.model_name)
            self._mdl = AutoModel.from_pretrained(self.model_name)
            self._mdl.eval()

    async def embed(self, texts: List[str]) -> List[List[float]]:
        if self.backend == "ollama":
            return await self._embed_ollama(texts)
        if self.backend == "transformers":
            return await asyncio.to_thread(self._embed_transformers, texts)
        # Fallback: simple hashing embedding (very weak); ensures system keeps working
        return [self._hash_embed(t) for t in texts]

    async def _embed_ollama(self, texts: List[str]) -> List[List[float]]:
        if not _ollama_available:
            return [self._hash_embed(t) for t in texts]
        out: List[List[float]] = []
        for t in texts:
            try:
                resp = ollama.embeddings(model=self.ollama_model, prompt=t)
                vec = resp.get("embedding") or []
                out.append([float(x) for x in vec])
            except Exception:
                out.append(self._hash_embed(t))
        return out

    def _embed_transformers(self, texts: List[str]) -> List[List[float]]:
        self._ensure_transformers()
        assert self._tok is not None and self._mdl is not None
        if torch is None:
            return [self._hash_embed(t) for t in texts]
        with torch.no_grad():
            enc = self._tok(texts, padding=True, truncation=True, return_tensors="pt")
            outputs = self._mdl(**enc)
            # Mean pool last hidden state
            last_hidden = outputs.last_hidden_state  # (B, T, H)
            attn_mask = enc["attention_mask"].unsqueeze(-1)  # (B, T, 1)
            masked = last_hidden * attn_mask
            sums = masked.sum(dim=1)
            counts = attn_mask.sum(dim=1).clamp(min=1)
            emb = sums / counts
            vecs = emb.cpu().tolist()
            return [[float(x) for x in v] for v in vecs]

    def _hash_embed(self, text: str, dim: int = 128) -> List[float]:
        # Simple hashing vector for fallback
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        # Repeat/truncate to desired dim
        arr = list(h) * ((dim + len(h) - 1) // len(h))
        arr = arr[:dim]
        # Normalize
        norm = math.sqrt(sum(x * x for x in arr)) or 1.0
        return [x / norm for x in arr]

    @staticmethod
    def cosine(a: List[float], b: List[float]) -> float:
        if not a or not b:
            return 0.0
        s = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) or 1.0
        nb = math.sqrt(sum(y * y for y in b)) or 1.0
        return float(max(-1.0, min(1.0, s / (na * nb))))


class SemanticRouter:
    """Lightweight semantic understanding for routing growth goals.

    It classifies if a text is an Instagram growth goal and extracts approximate
    parameters using loose extraction plus semantic similarity.
    """

    def __init__(self, engine: EmbeddingsEngine | None = None) -> None:
        self.engine = engine or EmbeddingsEngine()
        self._goal_seed = "instagram followers growth plan increase followers grow account strategy days niche"
        self._other_seed = "small talk greeting weather date time movie tech general chat entertainment"
        self._goal_vec: Optional[List[float]] = None
        self._other_vec: Optional[List[float]] = None

    async def _seed(self) -> None:
        if self._goal_vec is None or self._other_vec is None:
            vecs = await self.engine.embed([self._goal_seed, self._other_seed])
            self._goal_vec, self._other_vec = vecs[0], vecs[1]

    async def understand(self, text: str) -> Dict[str, Any]:
        await self._seed()
        assert self._goal_vec is not None and self._other_vec is not None
        [q_vec] = await self.engine.embed([text])
        sim_goal = self.engine.cosine(self._goal_vec, q_vec)
        sim_other = self.engine.cosine(self._other_vec, q_vec)
        is_goal = sim_goal > max(0.35, sim_other + 0.05)  # semantic threshold

        # Lightweight extraction (numbers/days/niche) as a fallback to strict regex
        import re
        days = None
        m_days = re.search(r"(\d{1,4})\s*days", text, flags=re.I)
        if m_days:
            try:
                days = int(m_days.group(1))
            except Exception:
                days = None
        # Followers from/to
        current = None
        target_increase = None
        m_range = re.search(r"from\s*(\d{1,9})\s*(?:followers)?\s*to\s*(\d{1,9})", text, flags=re.I)
        if m_range:
            try:
                a = int(m_range.group(1)); b = int(m_range.group(2))
                current = a
                target_increase = (b - a) / a if a > 0 else 1.0
            except Exception:
                pass
        if target_increase is None:
            m_pct = re.search(r"(\d{1,3})\s*%", text)
            if m_pct:
                try:
                    target_increase = float(m_pct.group(1)) / 100.0
                except Exception:
                    target_increase = None
        # Niche heuristic: words after in/for or trailing comma phrase
        niche = None
        m_niche = re.search(r"(?:in|for)\s+(?:the\s+)?([a-zA-Z][a-zA-Z\s]{2,40})", text)
        if m_niche:
            niche = m_niche.group(1).strip()
        else:
            parts = [p.strip() for p in text.split(',') if p.strip()]
            if parts:
                tail = parts[-1]
                if ' ' in tail or tail.isalpha():
                    niche = tail

        payload_suggestion: Dict[str, Any] | None = None
        if is_goal and (days is not None) and (target_increase is not None):
            payload_suggestion = {
                "target_metric": "followers",
                "target_increase": max(0.0, float(target_increase)),
                "timeline_days": int(days),
                "niche": niche or "general",
                "current_followers": int(current or 0),
                "notes": text,
            }

        return {
            "is_instagram_growth_goal": bool(is_goal),
            "similarity": float(sim_goal),
            "payload_suggestion": payload_suggestion,
            "extracted": {
                "days": days,
                "target_increase": target_increase,
                "current_followers": current,
                "niche": niche,
            },
        }

    async def relevance_scores(self, query: str, texts: List[str]) -> List[float]:
        [q_vec] = await self.engine.embed([query])
        docs = await self.engine.embed(texts)
        return [self.engine.cosine(q_vec, d) for d in docs]
