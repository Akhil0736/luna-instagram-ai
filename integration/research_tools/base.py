from __future__ import annotations

import abc
from typing import List

from integration.models import ResearchInsight


class ResearchTool(abc.ABC):
    """Abstract base for research tools that return ResearchInsight items."""

    name: str = "base"

    @abc.abstractmethod
    async def research(self, queries: List[str]) -> List[ResearchInsight]:
        raise NotImplementedError
