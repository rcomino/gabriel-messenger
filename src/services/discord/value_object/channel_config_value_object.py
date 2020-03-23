"""Channel Config Value Object."""

from dataclasses import dataclass
from typing import List, Dict

from src.services.discord.value_object.reporting_channel_config_value_object import \
    ReportingChannelConfigValueObject


@dataclass
class ChannelConfigValueObject:
    """Channel Config Value Object. Configuration of channel."""
    reactions: List[str]
    reporting_channels_config: Dict[int, ReportingChannelConfigValueObject]
