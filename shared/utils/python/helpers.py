import re
from typing import Iterable, List, TypeVar, Union

T = TypeVar("T")


def slugify(text: str) -> str:
    """Create a filesystem and URL friendly slug from text.

    Example:
        >>> slugify("Hello, World!")
        'hello-world'
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def ensure_list(value: Union[T, Iterable[T], None]) -> List[T]:
    """Ensure the given value is returned as a list (without exploding strings).

    Example:
        >>> ensure_list(1)
        [1]
        >>> ensure_list([1, 2])
        [1, 2]
        >>> ensure_list(None)
        []
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]  # type: ignore[list-item]
