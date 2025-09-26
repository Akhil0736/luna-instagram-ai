"""Core agent abstractions for the implementation layer."""
from abc import ABC, abstractmethod
from typing import Any, Dict

class AgentBase(ABC):
    """Defines the core contract every Luna implementation agent must follow."""

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from the provided context."""
        raise NotImplementedError
