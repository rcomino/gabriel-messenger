"""Author Value Object Module."""

from dataclasses import dataclass


@dataclass
class AuthorValueObject:
    """Author Value object. This value object descrives author of something."""
    name: str = None
    url: str = None
    icon_url: str = None
