"""Reporting Channel Reaction Change Config Value Object Module."""
from dataclasses import dataclass


@dataclass
class ReactionChangeConfig:
    """Reporting Channel Reaction Change Config Value Object. Configuration when someone add or remove a reaction of a
    event message."""
    text: str = None
    points: int = 0
