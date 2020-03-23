"""Reporting Channel Config Value Object Module"""
from dataclasses import dataclass
from typing import List, Dict

from src.ser.discord.data.reaction_config import \
    ReactionConfig


@dataclass
class ReportingChannelConfig:
    """Reporting Channel Config Value Object Module. Reporting Channel Config."""
    reactions: Dict[str, ReactionConfig]
    description: str
    footer: List[str]
