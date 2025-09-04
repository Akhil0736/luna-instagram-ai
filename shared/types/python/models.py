from dataclasses import dataclass
from typing import Optional


@dataclass
class UserProfile:
    """Shared user profile representation used across services.

    Keep this file free from runtime dependencies (std lib only), so all repos can import it.
    """

    id: str
    display_name: str
    email: Optional[str] = None
