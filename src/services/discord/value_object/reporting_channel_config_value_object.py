"""Reporting Channel Config Value Object Module"""
from dataclasses import dataclass
from typing import List, Dict

from src.services.discord.value_object.reporting_channel_reaction_config_value_object import \
    ReportingChannelReactionConfigValueObject


@dataclass
class ReportingChannelConfigValueObject:
    """Reporting Channel Config Value Object Module. Reporting Channel Config."""
    reactions: Dict[str, ReportingChannelReactionConfigValueObject]
    description: str
    footer: List[str]
