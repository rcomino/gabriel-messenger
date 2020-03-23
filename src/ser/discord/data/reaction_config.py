"""Reporting Channel Reaction Config Value Object Module."""

from dataclasses import dataclass

from src.ser.discord.data.reaction_change_config import \
    ReactionChangeConfig


@dataclass
class ReactionConfig:
    """Reporting Channel Reaction Change Config Value Object. Configuration when someone add or remove a reaction of a
    event message."""
    text: str
    reaction_add: ReactionChangeConfig
    reaction_remove: ReactionChangeConfig
